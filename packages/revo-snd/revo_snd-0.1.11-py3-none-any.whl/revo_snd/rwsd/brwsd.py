import io
from itertools import repeat

from revo_snd.nw4r import *


class _Version:
    VERSION_1_0 = 0x0100
    VERSION_1_1 = 0x0101  # bugfix and changes to the WAV block
    VERSION_1_2 = 0x0102  # ??
    VERSION_1_3 = 0x0103  # uses WAV archives (BRWAR) instead of own WAV block


# Currently, I cannot be bothered implementing more than
# necessary to work for NSMB Wii
SUPPORTED_VERSIONS = {_Version.VERSION_1_3}


class _WsdInfo:
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            self._read_from_file(data)
        else:
            self.pitch = 1.0
            self.pan = 64
            self.surround_pan = 0
            self.fx_send_a = 0
            self.fx_send_b = 0
            self.fx_send_c = 0
            self.main_send = 127

    def _read_from_file(self, data: BinaryIO) -> None:
        (self.pitch, self.pan, self.surround_pan, self.fx_send_a, self.fx_send_b, self.fx_send_c,
         self.main_send, _) = struct.unpack('>fBBBBBBH', data.read(12))

        read_nw4r_ref(data)  # Null reference
        read_nw4r_ref(data)  # Null reference
        data.read(4)  # padding

    def __bytes__(self) -> bytes:
        return struct.pack('>fBBBBBBH16sI',
                           self.pitch, self.pan, self.surround_pan, self.fx_send_a, self.fx_send_b,
                           self.fx_send_c, self.main_send, 0, NW4R_EMPTY_REFERENCE * 2, 0)

    def __str__(self) -> str:
        return (f'<WsdInfo(pitch={round(self.pitch, 4)}, pan={self.pan}, surround_pan={self.surround_pan}, '
                f'fx_send_A={self.fx_send_a}, fx_send_B={self.fx_send_b}, fx_send_C={self.fx_send_c}, '
                f'main_send={self.main_send})>')

    def __repr__(self) -> str:
        return self.__str__()


@dataclasses.dataclass
class _NoteEvent:
    position: float = 0.0
    length: float = 0.0
    note_idx: int = 0

    def __bytes__(self) -> bytes:
        return struct.pack('>ffII', self.position, self.length, self.note_idx, 0)

    @classmethod
    def read_from_file(cls, data: BinaryIO) -> Self:
        position, length, note_idx, _ = struct.unpack('>ffII', data.read(16))
        return cls(position, length, note_idx)


class _TrackInfo:
    def __init__(self, data: BinaryIO = None, data_off: int = 0) -> None:
        if data is not None:
            self._read_from_file(data, data_off)
        else:
            self.note_events = []

    def to_bytes(self, track_info_offset: int) -> bytes:
        buffer = io.BytesIO()

        # Align offset to start of DATA section
        buffer.write(NW4R_BUILD_BYTES_FOR_REF(track_info_offset + 8))

        buffer.write(len(self.note_events).to_bytes(length=4))

        refs_pos = buffer.tell()
        buffer.write(NW4R_EMPTY_REFERENCE * len(self.note_events))

        offset_to_data = buffer.tell() + track_info_offset
        offsets = []
        for note in self.note_events:
            offsets.append(offset_to_data)
            buffer.write(bytes(note))

            padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
            buffer.write(b'\x00' * padding_size)

            offset_to_data = buffer.tell() + track_info_offset

        buffer.seek(refs_pos)
        [buffer.write(NW4R_BUILD_BYTES_FOR_REF(off)) for off in offsets]

        return buffer.getvalue()

    def _read_from_file(self, data: BinaryIO, data_off: int) -> None:
        note_event_tbl_ref = read_nw4r_ref(data)

        data.seek(get_offset_from_ref(note_event_tbl_ref, data_off))
        tbl_len, = struct.unpack('>I', data.read(4))

        self.note_events = []
        for ref in [read_nw4r_ref(data) for _ in repeat(None, tbl_len)]:
            if ref is not None:
                data.seek(get_offset_from_ref(ref, data_off))
                self.note_events.append(_NoteEvent.read_from_file(data))
            else:
                self.note_events.append(None)

    def __str__(self) -> str:
        return f'<WsdTrackInfo(note_events={self.note_events})>'

    def __repr__(self) -> str:
        return self.__str__()


class _TrackTable:
    def __init__(self, data: BinaryIO = None, data_off: int = 0) -> None:
        if data is not None:
            self._read_from_file(data, data_off)
        else:
            self.trk_info = []

    def to_bytes(self, base_offset: int) -> bytes:
        buffer = io.BytesIO()

        buffer.write(len(self.trk_info).to_bytes(length=4))

        refs_pos = buffer.tell()
        buffer.write(NW4R_EMPTY_REFERENCE * len(self.trk_info))

        offset_to_data = buffer.tell() + base_offset

        offsets = []
        for trk in self.trk_info:
            offsets.append(offset_to_data)
            buffer.write(trk.to_bytes(offset_to_data))

            # Align to 0x4 bytes
            padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
            buffer.write(b'\x00' * padding_size)

            offset_to_data = buffer.tell() + base_offset + 0x20

        buffer.seek(refs_pos)
        [buffer.write(NW4R_BUILD_BYTES_FOR_REF(off)) for off in offsets]

        return buffer.getvalue()

    def _read_from_file(self, data: BinaryIO, data_off) -> None:
        tbl_size, = struct.unpack('>I', data.read(4))

        self.trk_info = []
        for ref in [read_nw4r_ref(data) for _ in repeat(None, tbl_size)]:
            if ref is not None:
                data.seek(get_offset_from_ref(ref, data_off))
                self.trk_info.append(_TrackInfo(data, data_off))
            else:
                self.trk_info.append(None)


@dataclasses.dataclass
class _NoteInfo:
    wave_idx: int
    attack: int = 127
    decay: int = 127
    sustain: int = 127
    release: int = 127
    hold: int = 0

    original_key: int = 60
    volume: int = 127
    pan: int = 64
    surround_pan: int = 0

    pitch: float = 1.0

    def __bytes__(self) -> bytes:
        return struct.pack('>iBBBBB3sBBBBf24sI',
                           self.wave_idx, self.attack, self.decay, self.sustain, self.release, self.hold,
                           b'\x00\x00\x00', self.original_key, self.volume, self.pan, self.surround_pan,
                           self.pitch, b'\x00' * 24, 0)

    @classmethod
    def read_from_file(cls, data: BinaryIO) -> Self:
        (wave_idx, attack, decay, sustain, release, hold, _,
         orig_key, volume, pan, surround_pan, pitch) = struct.unpack('>iBBBBB3sBBBBf', data.read(20))

        read_nw4r_ref(data)  # NULL
        read_nw4r_ref(data)  # NULL
        read_nw4r_ref(data)  # NULL

        data.read(4)  # padding

        return cls(wave_idx, attack, decay, sustain, release, hold, orig_key, volume, pan, surround_pan, pitch)


class _Wsd:
    def __init__(self, data: BinaryIO = None, data_off: int = 0) -> None:
        if data is not None:
            self._read_from_file(data, data_off)
        else:
            self.wsd_info = _WsdInfo()
            self.trk_tbl = _TrackTable()
            self.note_tbl = []

    def _read_from_file(self, data: BinaryIO, data_off: int) -> None:
        wsd_info_ref, trk_tbl_ref, note_tbl_ref = read_nw4r_ref(data), read_nw4r_ref(data), read_nw4r_ref(data)

        data.seek(get_offset_from_ref(wsd_info_ref, data_off))
        self.wsd_info = _WsdInfo(data)

        data.seek(get_offset_from_ref(trk_tbl_ref, data_off))
        self.trk_tbl = _TrackTable(data, data_off)

        data.seek(get_offset_from_ref(note_tbl_ref, data_off))
        tbl_len, = struct.unpack('>I', data.read(4))
        self.note_tbl = []

        for ref in [read_nw4r_ref(data) for _ in repeat(None, tbl_len)]:
            if ref is not None:
                data.seek(get_offset_from_ref(ref, data_off))
                self.note_tbl.append(_NoteInfo.read_from_file(data))
            else:
                self.note_tbl.append(None)

    def to_bytes(self, base_offset: int) -> bytes:
        buffer = io.BytesIO()
        buffer.write(NW4R_EMPTY_REFERENCE * 3)

        wsd_info_off = buffer.tell() + base_offset - 0x8
        buffer.write(bytes(self.wsd_info))

        trk_tbl_off = buffer.tell() + base_offset - 0x8
        buffer.write(self.trk_tbl.to_bytes(trk_tbl_off))

        note_tbl_off = buffer.tell() + base_offset - 0x8
        buffer.write(len(self.note_tbl).to_bytes(length=4))

        note_refs = buffer.tell()
        buffer.write(NW4R_EMPTY_REFERENCE * len(self.note_tbl))

        offsets = []
        for note_info in self.note_tbl:
            offsets.append(buffer.tell())
            buffer.write(bytes(note_info))

            # Align to 0x4 bytes
            padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
            buffer.write(b'\x00' * padding_size)

        buffer.seek(0)

        buffer.write(NW4R_BUILD_BYTES_FOR_REF(wsd_info_off))
        buffer.write(NW4R_BUILD_BYTES_FOR_REF(trk_tbl_off))
        buffer.write(NW4R_BUILD_BYTES_FOR_REF(note_tbl_off))

        buffer.seek(note_refs)
        for off in offsets:
            buffer.write(NW4R_BUILD_BYTES_FOR_REF(off - 8 + base_offset))

        return buffer.getvalue()

    def __str__(self) -> str:
        return f'<WSD(wsd_info={self.wsd_info})>'

    def __repr__(self) -> str:
        return self.__str__()


class _Data:
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            self._read_from_file(data)
        else:
            self.wsd = []

    def append(self, wave_idx: int) -> None:
        wsd = _Wsd()

        track_info = _TrackInfo()
        track_info.note_events.append(_NoteEvent())

        wsd.trk_tbl.trk_info.append(track_info)
        wsd.note_tbl.append(_NoteInfo(wave_idx))

        self.wsd.append(wsd)

    def _read_from_file(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        header = read_nw4r_block_header(data)
        block_sanity_check(header.magic, 'DATA')

        wsd_cnt, = struct.unpack('>I', data.read(4))
        self.wsd = []
        for ref in [read_nw4r_ref(data) for _ in repeat(None, wsd_cnt)]:
            if ref is not None:
                data.seek(get_offset_from_ref(ref, self._base_offset))
                self.wsd.append(_Wsd(data, self._base_offset))
            else:
                self.wsd.append(None)

    def __bytes__(self) -> bytes:
        buffer = io.BytesIO()
        buffer.write(b'DATA\x00\x00\x00\x00')

        buffer.write(len(self.wsd).to_bytes(length=4))

        refs_off = buffer.tell()
        buffer.write(NW4R_EMPTY_REFERENCE * len(self.wsd))

        offset_to_data = buffer.tell()
        offsets = []
        for wsd in self.wsd:
            offsets.append(offset_to_data)

            buffer.write(wsd.to_bytes(buffer.tell()))

            offset_to_data = buffer.tell()

        buf_old = buffer.tell()
        buffer.seek(refs_off)
        for off in offsets:
            buffer.write(NW4R_BUILD_BYTES_FOR_REF(off - 8))

        buffer.seek(buf_old)
        #padding_size = (0xF - (buffer.tell() % 0xF)) % 0xF
        #buffer.write(b'\x00' * padding_size)

        # Align to 0x20 bytes
        buffer.write(b'\x00' * (align_up(buffer.tell(), 0x20) - buffer.tell()))

        data_chunk_size = buffer.tell()

        buffer.seek(0x4)
        buffer.write(data_chunk_size.to_bytes(length=4))

        return buffer.getvalue()


class BRWSD(RevFile):
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            self._read_from_file(data)

    def _read_from_file(self, data: BinaryIO) -> None:
        self.base_offset = data.tell()

        self.file_info = read_nw4r_file_header(data)
        file_sanity_check(self.file_info.magic, self.file_info.byte_order, self.file_info.version,
                          FileTag.BRWSD, SUPPORTED_VERSIONS)
        self._file_size = self.file_info.file_size

        self.data_off, self.data_size, self.wav_off, self.wav_size = struct.unpack('>IIII', data.read(16))
        self.data_off += self.base_offset

        data.seek(self.data_off)
        self._data_block = _Data(data)

        data.seek(self.base_offset)
        self.raw_data = data.read(self._file_size)

        # Restore state to the expected position of the reader
        data.seek(self.base_offset + self.size)

    def append(self, wav_idx: int) -> None:
        self._data_block.append(wav_idx)

    def __bytes__(self) -> bytes:
        # We won't write WAV block, only version 1.3 BRWSD files
        buffer = io.BytesIO()
        buffer.write(struct.pack('>4sHHIHHIIII', FileTag.BRWSD.encode('ascii'), ByteOrder.BIG_ENDIAN,
                                 _Version.VERSION_1_3, 0, 0x20, 1, 0x20, 0, 0, 0))

        data = bytes(self._data_block)
        buffer.write(data)

        buffer.write(b'\x00' * (align_up(buffer.tell(), 0x20) - buffer.tell()))
        file_size = buffer.tell()

        buffer.seek(0x08)
        buffer.write(file_size.to_bytes(length=4))

        buffer.seek(0x14)
        buffer.write(len(data).to_bytes(length=4))
        return buffer.getvalue()

    def __getitem__(self, item: int) -> list[_NoteInfo | None]:
        if not isinstance(item, int):
            raise IndexError('Can only access elements in BRWSD files with an idx of type "int"')

        wsd = self._data_block.wsd
        if not (0 <= item < len(wsd)):
            raise IndexError(f'BRWSD index out of bounds. Only allowed indices in the range of [0 - {len(wsd) - 1}]')

        return self._data_block.wsd[item].note_tbl

    @classmethod
    def from_file(cls, data: (str | BinaryIO), *args, **kwargs) -> Self:
        return cls(open(data, 'rb')) if isinstance(data, str) else cls(data)
