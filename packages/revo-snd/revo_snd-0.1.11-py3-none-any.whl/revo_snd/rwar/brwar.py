import io
import struct
from typing import Tuple, Any

from revo_snd.nw4r import *
from revo_snd.rwav.brwav import BRWAV


class _Version:
    VERSION_1_0 = 0x0100


SUPPORTED_VERSIONS = {_Version.VERSION_1_0}


class _TableEntry:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self.wav_ref = read_nw4r_ref(data)
            self.wav_size = struct.unpack('>I', data.read(4))


class _Table:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        block_info = read_nw4r_block_header(data)
        block_sanity_check(block_info.magic, 'TABL')

        n_entry, = struct.unpack('>I', data.read(4))
        self.entries = [_TableEntry(data) for _ in range(n_entry)]


class _Data:
    def __init__(self, data: BinaryIO, __tbl: _Table) -> None:
        self.wavs = []

        if data is not None:
            self._read_from_data(data, __tbl)

    def _read_from_data(self, data: BinaryIO, __tbl: _Table) -> None:
        self._base_offset = data.tell()
        self.__tbl = __tbl

        block_info = read_nw4r_block_header(data)
        assert block_info.magic == 'DATA', \
            f'Incorrect BRWAR DATA magic, expected "DATA" but read "{block_info.magic}" instead'

        data.read(24)  # skip padding
        self.wavs = [self.__get_rwav0(i, data) for i in range(len(__tbl.entries))]

    def __get_rwav0(self, idx: int, __buffer: BinaryIO) -> BRWAV:
        __ref = self.__tbl.entries[idx].wav_ref
        __buffer.seek(__ref.offset + self._base_offset)

        offset = __buffer.tell()
        rwav = BRWAV(__buffer)
        rwav.base_offset = offset

        return rwav


class BRWAR(RevFile):
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._load_from_data(data)

    def __getitem__(self, key: int) -> BRWAV:
        return self.wavs[key]

    def get_wav_by_offset(self, offset: int) -> (tuple[int, BRWAV] | None):
        for idx, wav in enumerate(self.wavs):
            if wav.base_offset == offset:
                return idx, wav

    def replace(self, idx: int, new_wav: BRWAV) -> None:
        if not (0 <= idx < len(self.wavs)):
            raise IndexError(f'Index {idx} out of bounds for BRWAR of size {len(self.wavs)}')

        self.wavs[idx] = new_wav

    def _load_from_data(self, data: BinaryIO) -> None:
        self.base_offset = data.tell()
        self._base_offset = data.tell()
        self.file_info = read_nw4r_file_header(data)

        file_sanity_check(self.file_info.magic, self.file_info.byte_order, self.file_info.version, FileTag.BRWAR, SUPPORTED_VERSIONS)
        self._file_size = self.file_info.file_size

        self.tbl_off, self.tbl_size, self.data_off, self.data_size = struct.unpack('>IIII', data.read(16))

        data.seek(self._base_offset + self.tbl_off)
        _tbl = _Table(data)

        data.seek(self._base_offset + self.data_off)
        _data = _Data(data, _tbl)

        data.seek(self._base_offset)
        self.wavs = _data.wavs

        # Restore state to the expected position of the reader
        data.seek(self._base_offset + self.size)

    def __len__(self) -> int:
        return len(self.wavs)

    def __bytes__(self) -> bytes:
        buffer = io.BytesIO()
        buffer.write(struct.pack('>4sHHIHHIIII', b'RWAR', ByteOrder.BIG_ENDIAN, _Version.VERSION_1_0,
                                 0, 0x20, 2,
                                 0x20, 0,  # TABL offset always 0x20
                                 0, 0))

        # Write TABL section
        buffer.write(b'TABL\x00\x00\x00\x00' + len(self.wavs).to_bytes(length=4))
        buffer.write((b'\x00' * (NW4R_SIZE_OF_REFERENCE + 4)) * len(self.wavs))  # Fill in later
        buffer.write(b'\x00' * (align_up(buffer.tell(), 0x20) - buffer.tell()))

        table_chunk_size = buffer.tell() - 0x20
        data_chunk_off = buffer.tell()

        buffer.seek(0x20 + 0x4)
        buffer.write(table_chunk_size.to_bytes(length=4))

        # Write DATA section
        buffer.seek(data_chunk_off)
        buffer.write(b'DATA\x00\x00\x00\x00' + (b'\x00' * 0x18))
        offsets = []

        for idx, wav in enumerate(self.wavs):
            offsets.append((wav.size, buffer.tell()))
            buffer.write(bytes(wav))
            buffer.write(b'\x00' * (align_up(buffer.tell(), 0x20) - buffer.tell()))

        buffer.write(b'\x00' * (align_up(buffer.tell(), 0x20) - buffer.tell()))
        file_size = buffer.tell()
        data_chunk_size = buffer.tell() - data_chunk_off

        buffer.seek(0x2C)
        for wav_size, offset in offsets:
            buffer.write(struct.pack('>BBHII', 1, 0, 0, offset - data_chunk_off, wav_size))

        # Write file size
        buffer.seek(0x08)
        buffer.write(file_size.to_bytes(length=4))

        # Write TABL size, DATA offset, DATA size
        buffer.seek(0x14)
        buffer.write(struct.pack('>III', table_chunk_size, data_chunk_off, data_chunk_size))
        return buffer.getvalue()

    @classmethod
    def from_file(cls, data: BinaryIO, *args, **kwargs) -> Self:
        return cls(data)
