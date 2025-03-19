# Nin0's at it again! Sending me through hell
# reimplementing the BRBNK files
import enum
from typing import List

from revo_snd.nw4r import *


class _Version:
    VERSION_1_0 = 0x0100
    VERSION_1_1 = 0x0101  # Support for volume in instrument data
    VERSION_1_2 = 0x0102  # Support for external WAV archive (see BRWAR) instead of embedded WAV block


SUPPORTED_VERSIONS = {_Version.VERSION_1_0, _Version.VERSION_1_1, _Version.VERSION_1_2}


class WavDataLocationType(enum.IntEnum):
    INDEX = 0
    ADDRESS = 1
    CALLBACK = 2  # it is possible, to embed a callback function, which then attaches the WAV to the BRBNK


class _RegionTableType(enum.IntEnum):
    INVALID = 0
    DIRECT = 1
    RANGE = 2
    INDEX = 3
    NULL = 4


class InstParam:
    def __init__(self, data: BinaryIO, version: int = _Version.VERSION_1_2) -> None:
        if data is not None:
            self._read_from_data(data, version)

    def _read_from_data(self, data: BinaryIO, version: int) -> None:
        (self.wav_no, self.atk, self.decay, self.sustain, self.release, self.hold, self.wav_dat_loc_type,
         self.note_off_type, self.alternate_assign, self.original_key, self.volume, self.pan, self.surround_pan,
         self.pitch) = struct.unpack('>IbbbbbBBBBBBBf', data.read(20))

        read_nw4r_ref(data)  # null_ref_1
        read_nw4r_ref(data)  # null_ref_2
        read_nw4r_ref(data)  # null_ref_3

        data.read(4)  # reserved

        if version < _Version.VERSION_1_1:
            self.volume = 127
            self.pitch = 1.0

        self.wav_dat_loc_type = WavDataLocationType(self.wav_dat_loc_type)

    def __str__(self) -> str:
        return f'<InstParam: wav_no={self.wav_no}, wav_loc_type={self.wav_dat_loc_type.name}, orig_key={self.original_key}, vol={self.volume}>'

    def __repr__(self) -> str:
        return self.__str__()


# Container class...
@dataclasses.dataclass
class RangeTable:
    ranges: list[range]
    instruments: list[InstParam]


@dataclasses.dataclass
class IndexTable:
    velocities: list[int]
    instruments: list[InstParam]


class _Data:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        block_info = read_nw4r_block_header(data)
        block_sanity_check(block_info.magic, 'DATA')

        tbl_len, = struct.unpack('>I', data.read(4))

        self.inst_tbl_off = data.tell()
        inst_ref_tbl = [read_nw4r_ref(data) for _ in range(tbl_len)]

        self.inst_data = inst_ref_tbl


class BRBNK(RevFile):
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_file(data)

    def _read_from_file(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()
        self.base_offset = self._base_offset
        self._data = data

        self.file_info = read_nw4r_file_header(data)
        file_sanity_check(self.file_info.magic, self.file_info.byte_order, self.file_info.version, FileTag.BRBNK, SUPPORTED_VERSIONS)
        self._file_size = self.file_info.file_size

        self.file_size = self.file_info.file_size
        self._data_off, self._data_size, self._wav_off, self._wav_size = struct.unpack('>IIII', data.read(16))

        self._data_off = self._base_offset + self._data_off
        data.seek(self._data_off)
        self._data_block = _Data(data)
        self._inst_data = self._data_block.inst_data

        self._data.seek(self._base_offset)
        self.raw_data = self._data.read(self.file_size)

        # Restore expected state after reading file
        data.seek(self._base_offset + self.file_size)

        #if self.file_info.version < _Version.VERSION_1_2:
        #    ...
            # too lazy to read WAV Blocks, coming soon I guess

        #self.wav_data = None

    def _get_ref(self, inst_ref: Reference, split_key: int) -> (Reference | None):
        data = self._data

        match inst_ref.data_type:
            case _RegionTableType.DIRECT:
                return inst_ref
            case _RegionTableType.RANGE:
                # We read a range table, defined as
                # RangeTable:
                #     u8 table_size
                #     u8 key[table_size]
                data.seek(get_offset_from_ref(inst_ref, self._data_off))

                tbl_off = data.tell()
                tbl_len, = struct.unpack('>B', data.read(1))
                tbl = list(struct.unpack(f'>{tbl_len}B', data.read(tbl_len)))

                idx = next((i for i, x in enumerate(tbl) if x < split_key), None)
                if idx is None:
                    return None

                ref_off = round_up(1 + tbl_len, 4) + (NW4R_SIZE_OF_REFERENCE * idx)
                data.seek(tbl_off + ref_off)

                return read_nw4r_ref(data)
            case _RegionTableType.INDEX:
                # We read an index table, defined as
                # IndexTable:
                #     u8 min
                #     u8 max
                #     u16 reserved
                #     InstRef ref[max - min + 1]
                # where InstRef is a reference to either a DirectInstrument,
                # RangedInstrument, IndexInstrument or void/null.
                data.seek(get_offset_from_ref(inst_ref, self._data_off))

                tbl_min, tbl_max, _ = struct.unpack('>BBH', data.read(4))
                if split_key < tbl_min or split_key > tbl_max:
                    return None

                tbl = [read_nw4r_ref(data) for _ in range(tbl_max - tbl_min + 1)]
                return tbl[split_key - tbl_min]
            case _RegionTableType.INVALID:
                return None
            case _:
                return None

    def get_inst_param(self, prg_no: int, key: int, velocity: int) -> (InstParam | None):
        if prg_no < 0 or prg_no >= len(self._inst_data):
            raise KeyError(f'BRBNK Error: Cannot load instrument with prg_no {prg_no}! It is out of bounds!')

        # Key region
        inst_ref = self._inst_data[prg_no]
        if inst_ref.data_type == _RegionTableType.NULL:
            return None

        if inst_ref.data_type != _RegionTableType.DIRECT:
            inst_ref = self._get_ref(inst_ref, key)
            if inst_ref is None:
                return None

        # Velocity region
        if inst_ref.data_type == _RegionTableType.NULL:
            return None

        if inst_ref.data_type != _RegionTableType.DIRECT:
            inst_ref = self._get_ref(inst_ref, velocity)
            if inst_ref is None:
                return None

        # Single region underneath the velocity region
        if inst_ref.data_type != _RegionTableType.DIRECT:
            return None

        self._data.seek(get_offset_from_ref(inst_ref, self._data_off))
        return InstParam(self._data)

    def get_inst_param_direct(self, prg_no: (int | list[int]), *, keep_structs: bool = False) -> (InstParam | list[InstParam] | None):
        """
        Returns the instrument data directly without going through the sound engine's
        way of picking/playing a sound. The advantage of this function over the normal
        get_inst_param is, that for ranged/index instruments, all InstParameters are
        returned inside a list.

        :param prg_no:       One or any number of instrument ids to load.
        :param keep_structs: (Optional) If true, Ranged/IndexTables will not be unpacked
        """

        def get_inst_data_for_prg(prg: int) -> None | InstParam | RangeTable | list[InstParam]:
            if prg < 0 or prg >= len(self._inst_data):
                raise KeyError(f'BRBNK Error: Cannot load instrument with prg_no {prg}! It is out of bounds!')

            inst_ref = self._inst_data[prg]
            if inst_ref is None:
                return None

            match inst_ref.data_type:
                case _RegionTableType.NULL | _RegionTableType.INVALID:
                    return None
                case _RegionTableType.DIRECT:
                    self._data.seek(get_offset_from_ref(inst_ref, self._data_off))
                    return InstParam(self._data)
                case _RegionTableType.RANGE:
                    # We read a range table, defined as
                    # RangeTable:
                    #     u8 table_size
                    #     u8 key[table_size]
                    self._data.seek(get_offset_from_ref(inst_ref, self._data_off))

                    tbl_off = self._data.tell()
                    tbl_len, = struct.unpack('>B', self._data.read(1))
                    tbl = list(struct.unpack(f'>{tbl_len}B', self._data.read(tbl_len)))

                    params = []
                    for idx in range(len(tbl)):
                        self._data.seek(tbl_off + (round_up(1 + tbl_len, 4) + (NW4R_SIZE_OF_REFERENCE * idx)))
                        ref = read_nw4r_ref(self._data)

                        self._data.seek(get_offset_from_ref(ref, self._data_off))
                        params.append(InstParam(self._data))

                    if keep_structs:
                        starts = [0] + [b + 1 for b in tbl[:-1]]
                        ranges = [range(start, bound + 1) for start, bound in zip(starts, tbl)]

                        return RangeTable(ranges, params)

                    return params
                case _RegionTableType.INDEX:
                    # We read an index table, defined as
                    # IndexTable:
                    #     u8 min
                    #     u8 max
                    #     u16 reserved
                    #     InstRef ref[max - min + 1]
                    # where InstRef is a reference to either a DirectInstrument,
                    # RangedInstrument, IndexInstrument or void/null.
                    self._data.seek(get_offset_from_ref(inst_ref, self._data_off))

                    tbl_min, tbl_max, _ = struct.unpack('>BBH', self._data.read(4))

                    tbl = [read_nw4r_ref(self._data) for _ in range(tbl_max - tbl_min + 1)]
                    params = []

                    for ref in tbl:
                        self._data.seek(get_offset_from_ref(ref, self._data_off))
                        params.append(InstParam(self._data))

                    if keep_structs:
                        return IndexTable(tbl, params)

                    return params

        if isinstance(prg_no, list):
            if not prg_no:
                return None

            result = []
            for __id in prg_no:
                __tmp = get_inst_data_for_prg(__id)
                if isinstance(__tmp, list):
                    result += __tmp
                else:
                    result.append(__tmp)
            return result

        return get_inst_data_for_prg(prg_no)

    def __bytes__(self) -> bytes:
        return self.raw_data

    @classmethod
    def from_file(cls, data: BinaryIO, *args, **kwargs) -> Self:
        return cls(data)
