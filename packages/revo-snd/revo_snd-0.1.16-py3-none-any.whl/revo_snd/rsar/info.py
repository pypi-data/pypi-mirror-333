import io
from itertools import repeat

from revo_snd.nw4r import *
from revo_snd.rsar.file import File

INFO_SEQ_SND_INFO_SIZE = 20
INFO_STRM_SND_INFO_SIZE = 12
INFO_WAV_SND_INFO_SIZE = 16


class _SoundType(enum.IntEnum):
    INVALID = 0
    SEQ = 1
    STRM = 2
    WAVE = 3


class Sound3DParam:
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            self.flags, self.decay_curve, self.decay_ratio, self.doppler_factor, _, _ = (
                struct.unpack('>IBBBBI', data.read(12)))
        else:
            self.flags = 0
            self.decay_curve = 1
            self.decay_ratio = 128
            self.doppler_factor = 0

    def __bytes__(self) -> bytes:
        return struct.pack('>IBBBBI', self.flags, self.decay_curve, self.decay_ratio, self.doppler_factor,
                           0, 0)

    def __str__(self) -> str:
        return (f'<Sound3DParam(flags={self.flags}, decay_curve={self.decay_curve}, decay_ration={self.decay_ratio}, '
                f'doppler_factor={self.doppler_factor})>')

    def __repr__(self) -> str:
        return self.__str__()


class _SeqSoundInfo:
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            self.seq_lbl_off, self.bnk_idx, self.alloc_track, self.seq_chn_priority, self.release_priority_fix, _, _ = (
                struct.unpack('>IIIBBHI', data.read(20)))

    def __bytes__(self) -> bytes:
        return struct.pack('>IIIBBHI', self.seq_lbl_off, self.bnk_idx, self.alloc_track,
                           self.seq_chn_priority, self.release_priority_fix, 0, 0)

    def __str__(self) -> str:
        return f'<SeqSoundInfo: LabelOffset=0x{self.seq_lbl_off:X}, BnkIdx={self.bnk_idx}, AllocTrack={self.alloc_track}>'

    def __repr__(self) -> str:
        return self.__str__()


class WaveSoundInfo:
    def __init__(self, data: BinaryIO = None, *, wave_idx: int = 0) -> None:
        if data is not None:
            self.wave_idx, self.alloc_track, self.chn_priority, self.release_priority_fix, _, _ = (
                struct.unpack('>iIBBHI', data.read(16)))
        else:
            self.wave_idx = wave_idx
            self.alloc_track = 1
            self.chn_priority = 64
            self.release_priority_fix = 0

    def __bytes__(self) -> bytes:
        return struct.pack('>iIBBHI', self.wave_idx, self.alloc_track, self.chn_priority, self.release_priority_fix, 0,
                           0)

    def __str__(self) -> str:
        return f'<WavSndInfo: wav_idx={self.wave_idx}, alloc_track={self.alloc_track}, chn_prio={self.chn_priority}>'

    def __repr__(self) -> str:
        return self.__str__()


class _StreamSoundInfo:
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            self.base_offset = data.tell()
            self.start_position, self.n_alloc_chn, self.alloc_track_flag, _ = struct.unpack('>IHHI', data.read(12))

    def __bytes__(self) -> bytes:
        return struct.pack('>IHHI', self.start_position, self.n_alloc_chn, self.alloc_track_flag, 0)

    def __str__(self) -> str:
        return f'<StrmSndInfo: start_pos={self.start_position}, n_alloc_chn={self.n_alloc_chn}, alloc_track_flag={self.alloc_track_flag}>'

    def __repr__(self) -> str:
        return self.__str__()


class SoundDataEntry:
    def __init__(self, data: BinaryIO = None, info_block_off: int = -1, *,
                 file_name_idx: int = -1, file_idx: int = -1, player_idx: int = 0, actor_ply_id: int = 0) -> None:
        if data is not None and info_block_off > -1:
            self._read_from_data(data, info_block_off)
        else:
            self.file_name_idx = file_name_idx
            self.file_idx = file_idx
            self.player_idx = player_idx

            self.volume = 90
            self.ply_priority = 64
            self.remote_filter = self.user_param1, self.user_param2, self.pan_mode, self.pan_curve = 0
            self.actor_ply_id = actor_ply_id

    def _read_from_data(self, data: BinaryIO, info_block_off: int) -> None:
        base_offset = data.tell()

        self.file_name_idx, self.file_idx, self.player_idx = struct.unpack('>III', data.read(12))

        snd3d_ref = read_nw4r_ref(data)

        self.volume, self.ply_priority, self.snd_type, self.remote_filter = struct.unpack('>BBBB', data.read(4))
        self.snd_type = _SoundType(self.snd_type)

        snd_info_ref = read_nw4r_ref(data)

        self.user_param1, self.user_param2, self.pan_mode, self.pan_curve, self.actor_ply_id, _ = (
            struct.unpack('>IIBBBB', data.read(12)))

        data.seek(get_offset_from_ref(snd3d_ref, info_block_off))
        self.snd3d = Sound3DParam(data)

        # Update:
        #    The game seems to work, even if this datatype is
        #    set incorrectly.

        # Sanity check if everything was read correctly, if it was, both data types will be identical
        assert self.snd_type == _SoundType(snd_info_ref.data_type), \
            (f'Error while reading SoundDataEntry beginning at 0x{base_offset:X}:'
             f' mismatching sound_type and data_type of reference fields')

        data.seek(get_offset_from_ref(snd_info_ref, info_block_off))
        match self.snd_type:
            case _SoundType.SEQ:
                self.snd_info = _SeqSoundInfo(data)
            case _SoundType.STRM:
                self.snd_info = _StreamSoundInfo(data)
            case _SoundType.WAVE:
                self.snd_info = WaveSoundInfo(data)
            case _SoundType.INVALID | _:
                raise AssertionError(f'Invalid sound_type read for SoundDataEntry beginning at 0x{base_offset:X}')

    def to_bytes(self, detailed_off: int, sound_3d_off: int) -> bytes:
        data = struct.pack('>III8sBBBB8sIIBBBB',
                           self.file_name_idx, self.file_idx, self.player_idx,
                           b'\x01\x00\x00\x00' + sound_3d_off.to_bytes(length=4, byteorder='big'),
                           self.volume, self.ply_priority, self.snd_type, self.remote_filter,
                           b'\x01' + self.snd_type.to_bytes() + b'\x00\x00' + detailed_off.to_bytes(length=4, byteorder='big'),
                           self.user_param1, self.user_param2,
                           self.pan_mode, self.pan_curve, self.actor_ply_id, 0)

        return data + bytes(self.snd_info) + bytes(self.snd3d)

    def __str__(self) -> str:
        return f'<SoundDataEntry: FileNameIdx={self.file_name_idx}, FileIdx={self.file_idx}, Sound Type={self.snd_type}>'


class _SoundBankEntry:
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            # Bank idx always 0
            self.file_name_idx, self.file_idx, self.bnk_idx = struct.unpack('>III', data.read(12))

    def __bytes__(self) -> bytes:
        return struct.pack('>III', self.file_name_idx, self.file_idx, self.bnk_idx)

    def __str__(self) -> str:
        return f'<SoundBankEntry: StringIdx={self.file_name_idx}, FileIdx={self.file_idx}, BankIdx={self.bnk_idx}>'

    def __repr__(self) -> str:
        return self.__str__()


class _PlayerInfoEntry:
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            self.file_name_idx, self.n_playable_snd, _, _, self.heap_size, _ = (
                struct.unpack('>IBBHII', data.read(16)))

    def __bytes__(self) -> bytes:
        return struct.pack('>IBBHII', self.file_name_idx, self.n_playable_snd, 0, 0, self.heap_size, 0)

    def __str__(self) -> str:
        return f'<ActorPlayer(n_playable_sound={self.n_playable_snd}, heap_size={self.heap_size})>'

    def __repr__(self) -> str:
        return self.__str__()


class _FilePositionEntry:
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            self.grp_idx, self.idx = struct.unpack('>II', data.read(8))

    def __bytes__(self) -> bytes:
        return struct.pack('>II', self.grp_idx, self.idx)

    def __str__(self) -> str:
        return f'<FilePositionEntry: GroupIdx={self.grp_idx}, IdxInGroup={self.idx}>'

    def __repr__(self) -> str:
        return self.__str__()


class _FileEntry:
    def __init__(self, data: BinaryIO = None, info_offset: int = -1) -> None:
        if data is not None and info_offset > -1:
            self._read_from_data(data, info_offset)

    def _read_from_data(self, data: BinaryIO, info_offset: int) -> None:
        self._base_offset = data.tell()

        # file_size     = size of the file WITHOUT the audio data
        # wav_file_size = size of the audio data itself, NULL if it is a RSEQ or an external file
        # entry_num     = always -1
        self.file_size, self.wav_file_size, self.entry_num = struct.unpack('>IIi', data.read(12))

        ext_file_pth_ref = read_nw4r_ref(data)  # if it is an external file, ref to the path, otherwise NULL
        file_tbl_ref = read_nw4r_ref(data)  # if it is an embedded file, ref to the file table, otherwise NULL

        self.ext_file_pth = '<None>'
        self.file_tbl = []

        if ext_file_pth_ref is not None:
            data.seek(get_offset_from_ref(ext_file_pth_ref, info_offset))
            read_from = data.tell()
            read_to = get_offset_from_ref(file_tbl_ref, info_offset)

            chunk = data.read(read_to - read_from)
            null = chunk.find(b'\0')

            self.ext_file_pth = chunk.decode('ascii') if null == -1 else chunk[:null].decode('ascii')

        if file_tbl_ref is not None:
            data.seek(get_offset_from_ref(file_tbl_ref, info_offset))
            n_file_pos_entry, = struct.unpack('>I', data.read(4))

            file_pos_entry_refs = [read_offset_from_ref(data, info_offset) for _ in range(n_file_pos_entry)]
            for i in range(n_file_pos_entry):
                data.seek(file_pos_entry_refs[i])
                self.file_tbl.append(_FilePositionEntry(data))

    def to_bytes(self, offset_to_data: int) -> bytes:
        if self.ext_file_pth != '<None>':
            strlen = len(self.ext_file_pth)
            file_pth_data = self.ext_file_pth.encode('ascii')

            ext_file_path_off = offset_to_data - 8 + 0x1C  # 0x1C == sizeof(FileEntry)
            file_pth_ref = b'\x01\x00\x00\x00' + ext_file_path_off.to_bytes(length=4, byteorder='big')
        else:
            strlen = 0
            file_pth_data = b''
            file_pth_ref = b'\x00\x00\x00\x00\x00\x00\x00\x00'

        buffer = io.BytesIO()
        buffer.write(struct.pack('>IIi8s8s', self.file_size, self.wav_file_size, self.entry_num,
                                 file_pth_ref, b'\x00' * 8))

        buffer.write(file_pth_data)

        padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
        buffer.write(b'\x00' * padding_size)

        file_pos_tbl_off = (offset_to_data - 8 + 0x1C) + strlen + padding_size
        file_tbl_ref = b'\x01\x00\x00\x00' + file_pos_tbl_off.to_bytes(length=4, byteorder='big')

        # Build the reference table to all the entries
        buffer.write(len(self.file_tbl).to_bytes(length=4))

        offset_to_data = file_pos_tbl_off + 4 + (len(self.file_tbl) * NW4R_SIZE_OF_REFERENCE)
        for _ in repeat(None, len(self.file_tbl)):
            buffer.write(b'\x01\x00\x00\x00' + offset_to_data.to_bytes(length=4, byteorder='big'))
            offset_to_data += 8

        # Behind the ref table are is the actual file pos table
        for file in self.file_tbl:
            buffer.write(bytes(file))

        buffer.seek(0x14)
        buffer.write(file_tbl_ref)
        return buffer.getvalue()

    def __str__(self) -> str:
        return (f'<FileEntry(file_size={self.file_size}, audio_data_size={self.wav_file_size}, '
                f'external_file_pth={self.ext_file_pth}, file_table={self.file_tbl})>')


class _GroupTableEntry:
    def __init__(self, data: BinaryIO = None,
                 parent_file_offset: int = 0,
                 parent_audio_offset: int = 0,
                 file_data: File = None) -> None:
        self.file = None
        self.audio_file = None
        if data is not None:
            self.grp_idx, self.file_data_off, self.file_data_size, self.audio_data_off, self.audio_data_size, _ = (
                struct.unpack('>IIIIII', data.read(24)))

            if parent_audio_offset > 0:
                self.audio_file = file_data.offset_to_id(parent_audio_offset + self.audio_data_off)

            if parent_file_offset != 0:
                self.file = file_data.offset_to_id(parent_file_offset + self.file_data_off)

    def to_bytes(self, file_look_up: dict[int, int], grp_file_off: int, grp_audio_off: int) -> bytes:
        if file_look_up is not None:
            file_data_off = file_look_up[self.file] - grp_file_off if self.file is not None else 0
            audio_data_off = file_look_up[self.audio_file] - grp_audio_off if self.audio_file is not None else 0
        else:
            file_data_off = 0
            audio_data_off = 0

        return struct.pack('>IIIIII', self.grp_idx, file_data_off, self.file_data_size,
                           audio_data_off, self.audio_data_size, 0)

    def __str__(self) -> str:
        return (f'<GroupTableEntry: FileID={self.grp_idx}, DataOff=0x{self.file_data_off:X}, '
                f'AudioOff=0x{self.audio_data_off:X}>')

    def __repr__(self) -> str:
        return self.__str__()


class GroupDataEntry:
    def __init__(self, data: BinaryIO = None, info_offset: int = -1, file_data: File = None) -> None:
        self.file = None
        self.audio_file = None

        self.files = []
        self.audio_files = []

        if data is not None and info_offset > -1:
            self._read_from_data(data, info_offset, file_data)

    def _read_from_data(self, data: BinaryIO, info_offset: int, file_data: File) -> None:
        self._base_offset = data.tell()

        self.file_name_idx, self.entry_num = struct.unpack('>ii', data.read(8))
        ext_file_pth_ref = read_nw4r_ref(data)

        self.grp_file_off, self.grp_file_size, self.grp_audio_off, self.grp_audio_size = (
            struct.unpack('>IIII', data.read(16)))

        self.file = file_data.offset_to_id(self.grp_file_off)
        self.audio_file = file_data.offset_to_id(self.grp_audio_off)

        grp_tbl_ref = read_nw4r_ref(data)

        self.ext_file_pth = '<None>'
        self.grp_tbl = []

        # Load external file name if there is any
        if ext_file_pth_ref is not None:
            data.seek(get_offset_from_ref(ext_file_pth_ref, info_offset))
            self.ext_file_pth = read_terminated_string(data)

        data.seek(get_offset_from_ref(grp_tbl_ref, info_offset))
        n_grp_tbl_entry, = struct.unpack('>I', data.read(4))

        n_grp_tbl_entry_refs = [read_offset_from_ref(data, info_offset) for _ in range(n_grp_tbl_entry)]
        for i in range(n_grp_tbl_entry):
            data.seek(n_grp_tbl_entry_refs[i])
            entry = _GroupTableEntry(data, self.grp_file_off, self.grp_audio_off, file_data)

            if entry.file != 1 and entry.file not in self.files:
                self.files.append(entry.file)

            if entry.audio_file != -1 and entry.audio_file not in self.audio_files:
                self.audio_files.append(entry.audio_file)

            self.grp_tbl.append(entry)

    def to_bytes(self, offset_to_data: int, file_look_up: dict[int, int]) -> bytes:
        if self.ext_file_pth != '<None>':
            strlen = len(self.ext_file_pth)
            file_pth_data = self.ext_file_pth.encode('ascii')

            ext_file_path_off = offset_to_data - 8 + 0x28  # 0x28 == sizeof(GroupDataEntry)
            file_pth_ref = b'\x01\x00\x00\x00' + ext_file_path_off.to_bytes(length=4, byteorder='big')
        else:
            strlen = 0
            file_pth_data = b''
            file_pth_ref = b'\x00\x00\x00\x00\x00\x00\x00\x00'

        if file_look_up is not None:
            grp_file_off = file_look_up[self.file]
            grp_audio_off = file_look_up[self.audio_file]
        else:
            grp_file_off = 0
            grp_audio_off = 0

        buffer = io.BytesIO()
        buffer.write(struct.pack('>ii8sIIII8s', self.file_name_idx, -1,  # always -1
                                 file_pth_ref, grp_file_off, self.grp_file_size,
                                 grp_audio_off, self.grp_audio_size, b'\x00' * 8))

        buffer.write(file_pth_data)

        padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
        buffer.write(b'\x00' * padding_size)

        file_pos_tbl_off = (offset_to_data - 8 + 0x28) + strlen + padding_size
        file_tbl_ref = b'\x01\x00\x00\x00' + file_pos_tbl_off.to_bytes(length=4, byteorder='big')

        # Build the reference table to all the entries
        buffer.write(len(self.grp_tbl).to_bytes(length=4))

        refs_start = buffer.tell()
        buffer.write(b'\x00' * 8 * len(self.grp_tbl))

        offsets = []
        # Behind the ref table are is the actual file pos table
        for grp_entry in self.grp_tbl:
            offsets.append(buffer.tell() - 8)
            buffer.write(grp_entry.to_bytes(file_look_up, grp_file_off, grp_audio_off))

        buffer.seek(refs_start)
        [buffer.write(b'\x01\x00\x00\x00' + (offset + offset_to_data).to_bytes(length=4)) for offset in offsets]

        buffer.seek(0x20)
        buffer.write(file_tbl_ref)
        return buffer.getvalue()

    def __str__(self) -> str:
        return f'<Group: StrIdx={self.file_name_idx} DataOff=0x{self.grp_file_off:X} AudioOff=0x{self.grp_audio_off:X}>'

    def __repr__(self) -> str:
        return self.__str__()


class Info:
    def __init__(self, data: BinaryIO = None, file_data: File = None) -> None:
        self.n_entry = 0

        if data is not None:
            self._read_from_data(data, file_data)
        else:
            self.snd_arc_common_info = None
            self.snd_data = []
            self.player_data = []
            self.grp_data = []
            self.bnk_data = []
            self.file_data = []

    def _read_from_data(self, data: BinaryIO, file_data: File) -> None:
        self._base_offset = data.tell()
        self._file_data = file_data

        block_info = read_nw4r_block_header(data)
        block_sanity_check(block_info.magic, 'INFO')

        snd_tbl_off = read_offset_from_ref(data, self._base_offset)
        bnk_tbl_off = read_offset_from_ref(data, self._base_offset)
        ply_tbl_off = read_offset_from_ref(data, self._base_offset)
        file_tbl_off = read_offset_from_ref(data, self._base_offset)
        grp_tbl_off = read_offset_from_ref(data, self._base_offset)

        # Read arc common info first. the last 6 bytes are padding, so skip them
        data.seek(read_offset_from_ref(data, self._base_offset))
        self.snd_arc_common_info = struct.unpack('>HHHHHHH', data.read(14))

        # Collect sound data entries
        data.seek(snd_tbl_off)
        n_snd_entry, = struct.unpack('>I', data.read(4))

        snd_refs = [read_offset_from_ref(data, self._base_offset) for _ in range(n_snd_entry)]
        self.snd_data = []
        for i in range(n_snd_entry):
            data.seek(snd_refs[i])
            self.snd_data.append(SoundDataEntry(data, self._base_offset))

        self.n_entry += len(self.snd_data)

        # Collect bank data entries
        data.seek(bnk_tbl_off)
        n_bnk_entry, = struct.unpack('>I', data.read(4))

        bnk_refs = [read_offset_from_ref(data, self._base_offset) for _ in range(n_bnk_entry)]
        self.bnk_data = []
        for i in range(n_bnk_entry):
            data.seek(bnk_refs[i])
            self.bnk_data.append(_SoundBankEntry(data))

        self.n_entry += len(self.bnk_data)

        # Collect player data entries
        data.seek(ply_tbl_off)
        n_ply_entry, = struct.unpack('>I', data.read(4))

        ply_refs = [read_offset_from_ref(data, self._base_offset) for _ in range(n_ply_entry)]
        self.player_data = []
        for i in range(n_ply_entry):
            data.seek(ply_refs[i])
            self.player_data.append(_PlayerInfoEntry(data))

        self.n_entry += len(self.player_data)

        # Collect file data entries
        data.seek(file_tbl_off)
        n_file_entry, = struct.unpack('>I', data.read(4))

        file_refs = [read_offset_from_ref(data, self._base_offset) for _ in range(n_file_entry)]
        self.file_data = []
        for i in range(n_file_entry):
            data.seek(file_refs[i])
            self.file_data.append(_FileEntry(data, self._base_offset))

        self.n_entry += len(self.file_data)

        # Collect group data entries
        data.seek(grp_tbl_off)
        n_grp_entry, = struct.unpack('>I', data.read(4))
        grp_refs = [read_offset_from_ref(data, self._base_offset) for _ in range(n_grp_entry)]
        self.grp_data = []

        self.n_entry += len(self.grp_data)

        for i in range(n_grp_entry):
            data.seek(grp_refs[i])
            self.grp_data.append(GroupDataEntry(data, self._base_offset, file_data))

    def _write_snd_tbl(self, buffer: io.BytesIO, only_null: bool = False) -> int:
        snd_table_n_entries = len(self.snd_data)
        snd_table_size = 4 + (snd_table_n_entries * NW4R_SIZE_OF_REFERENCE)

        # Start writing SoundInfo RefTable
        snd_tbl_off = buffer.tell() - 8
        snd_tbl_start_off = buffer.tell() + snd_table_size

        if only_null:
            buffer.write(b'\x00\x00\x00\x00')
        else:
            buffer.write(snd_table_n_entries.to_bytes(length=4, byteorder='big'))

        offset_to_data = snd_tbl_start_off

        continue_at = 0
        for snd_info in self.snd_data:
            if only_null:
                buffer.write(b'\x00' * 8)
            else:
                buffer.write(b'\x01\x00\x00\x00' + (offset_to_data - 8).to_bytes(length=4, byteorder='big'))
            buf_old_pos = buffer.tell()

            # Go to actual offset and write the data.
            buffer.seek(offset_to_data)
            offset_to_detailed_sound = offset_to_data - 0x08 + 0x2C
            offset_to_sound_3d = offset_to_data - 0x08 + 0x2C

            match snd_info.snd_type:
                case _SoundType.SEQ:
                    offset_to_sound_3d += INFO_SEQ_SND_INFO_SIZE
                case _SoundType.STRM:
                    offset_to_sound_3d += INFO_STRM_SND_INFO_SIZE
                case _SoundType.WAVE:
                    offset_to_sound_3d += INFO_WAV_SND_INFO_SIZE
                case _:
                    raise ValueError('Unknown sound data type')

            data = snd_info.to_bytes(offset_to_detailed_sound, offset_to_sound_3d)
            if only_null:
                buffer.write(b'\x00' * len(data))
            else:
                buffer.write(data)

            continue_at = buffer.tell()
            buffer.seek(buf_old_pos)
            offset_to_data += len(data)

        buffer.seek(continue_at)
        padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
        buffer.write(b'\x00' * padding_size)

        return snd_tbl_off

    def _write_bnk_tbl(self, buffer: io.BytesIO, only_null: bool = False) -> int:
        bnk_table_n_entries = len(self.bnk_data)
        bnk_table_size = 4 + (bnk_table_n_entries * NW4R_SIZE_OF_REFERENCE)

        bnk_tbl_off = buffer.tell() - 8
        bnk_tbl_start_off = buffer.tell() + bnk_table_size

        # sizeof BnkEntry = 12
        if only_null:
            buffer.write(b'\x00' * (bnk_table_size + (bnk_table_n_entries * 12)))
            padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
            buffer.write(b'\x00' * padding_size)

            return bnk_tbl_off

        buffer.write(bnk_table_n_entries.to_bytes(length=4, byteorder='big'))

        continue_at = 0
        offset_to_data = bnk_tbl_start_off
        for bnk in self.bnk_data:
            buffer.write(b'\x01\x00\x00\x00' + (offset_to_data - 8).to_bytes(length=4, byteorder='big'))
            buf_old_pos = buffer.tell()

            buffer.seek(offset_to_data)
            data = bytes(bnk)

            buffer.write(data)
            continue_at = buffer.tell()
            buffer.seek(buf_old_pos)
            offset_to_data += len(data)

        buffer.seek(continue_at)
        padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
        buffer.write(b'\x00' * padding_size)

        return bnk_tbl_off

    def _write_ply_tbl(self, buffer: io.BytesIO, only_null: bool = False) -> int:
        ply_table_n_entries = len(self.player_data)
        ply_table_size = 4 + (ply_table_n_entries * NW4R_SIZE_OF_REFERENCE)

        ply_tbl_off = buffer.tell() - 8
        ply_tbl_start_off = buffer.tell() + ply_table_size

        # sizeof PlyEntry = 16
        if only_null:
            buffer.write(b'\x00' * (ply_table_size + (ply_table_n_entries * 16)))
            padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
            buffer.write(b'\x00' * padding_size)

            return ply_tbl_off

        buffer.write(ply_table_n_entries.to_bytes(length=4, byteorder='big'))

        continue_at = 0
        offset_to_data = ply_tbl_start_off
        for ply in self.player_data:
            buffer.write(b'\x01\x00\x00\x00' + (offset_to_data - 8).to_bytes(length=4, byteorder='big'))
            buf_old_pos = buffer.tell()

            buffer.seek(offset_to_data)
            data = bytes(ply)

            buffer.write(data)
            continue_at = buffer.tell()
            buffer.seek(buf_old_pos)
            offset_to_data += len(data)

        buffer.seek(continue_at)
        padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
        buffer.write(b'\x00' * padding_size)

        return ply_tbl_off

    def _write_file_tbl(self, buffer: io.BytesIO, only_null: bool = False) -> int:
        file_table_n_entries = len(self.file_data)

        file_tbl_off = buffer.tell() - 8

        if only_null:
            buffer.write(b'\x00\x00\x00\x00')
        else:
            buffer.write(file_table_n_entries.to_bytes(length=4, byteorder='big'))

        data_start = buffer.tell()
        # Write all empty references
        buffer.write((b'\x00' * NW4R_SIZE_OF_REFERENCE) * file_table_n_entries)

        offset_to_data = buffer.tell()
        offsets = []

        for file in self.file_data:
            offsets.append(offset_to_data)
            if only_null:
                data = file.to_bytes(offset_to_data)
                buffer.write(b'\x00' * len(data))
            else:
                buffer.write(file.to_bytes(offset_to_data))

            offset_to_data = buffer.tell()

        padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
        buffer.write(b'\x00' * padding_size)

        if only_null:
            return file_tbl_off

        buff_old = buffer.tell()
        buffer.seek(data_start)

        # NOW write all references
        for off in offsets:
            buffer.write(b'\x01\x00\x00\x00' + (off - 8).to_bytes(length=4))

        # Restore old state
        buffer.seek(buff_old)

        return file_tbl_off

    def _write_grp_tbl(self, buffer: io.BytesIO, file_look_up: dict[int, int] = None, only_null: bool = False) -> int:
        grp_table_n_entries = len(self.grp_data)

        grp_tbl_off = buffer.tell() - 8

        if only_null:
            buffer.write(b'\x00\x00\x00\x00')
        else:
            buffer.write(grp_table_n_entries.to_bytes(length=4, byteorder='big'))

        data_start = buffer.tell()
        # Write all empty references
        buffer.write((b'\x00' * NW4R_SIZE_OF_REFERENCE) * grp_table_n_entries)

        offset_to_data = buffer.tell()
        offsets = []

        for idx, grp in enumerate(self.grp_data):
            offsets.append(offset_to_data)

            if only_null:
                data = grp.to_bytes(offset_to_data, file_look_up)
                buffer.write(b'\x00' * len(data))
            else:
                buffer.write(grp.to_bytes(offset_to_data, file_look_up))

            offset_to_data = buffer.tell()

        padding_size = (0x4 - (buffer.tell() % 0x4)) % 0x4
        buffer.write(b'\x00' * padding_size)

        if only_null:
            return grp_tbl_off

        buff_old = buffer.tell()
        buffer.seek(data_start)

        # NOW write all references
        for off in offsets:
            buffer.write(b'\x01\x00\x00\x00' + (off - 8).to_bytes(length=4))

        # Restore old state
        buffer.seek(buff_old)

        return grp_tbl_off

    def to_bytes(self, rsar_buffer: io.BytesIO) -> tuple[int, int, int, int]:
        buffer = io.BytesIO()

        info_chunk_off = rsar_buffer.tell()

        # Write base header of INFO block (magic + block_size)
        buffer.write(b'INFO\x00\x00\x00\x00')

        # Pre-write all references to the different
        # sub-tables inside the INFO chunk:
        #    DataRef<SoundInfoTable>
        #    DataRef<BankInfoTable>
        #    DataRef<PlayerInfoTable>
        #    DataRef<FileInfoTable>
        #    DataRef<GroupInfoTable>
        #    DataRef<SoundArcInfo>
        buffer.write(b'\x00\x00\x00\x00\x00\x00\x00\x00' * 6)  # Empty references, will be written later

        # Write everything later
        snd_tbl_off = self._write_snd_tbl(buffer, True)
        bnk_tbl_off = self._write_bnk_tbl(buffer, True)
        ply_tbl_off = self._write_ply_tbl(buffer, True)
        file_tbl_off = self._write_file_tbl(buffer, True)
        grp_tbl_off = self._write_grp_tbl(buffer, None, True)
        arc_info_off = buffer.tell() - 8

        buffer.write(b'\x00' * 14)  # Pre-write arc_info
        buffer.write(b'\x00' * (align_up(buffer.tell(), 0x20) - buffer.tell()))
        info_chunk_size = buffer.tell()

        # Finalize INFO chunk
        # Now ACTUALLY write the data
        #
        # We write the INFO and FILE section in conjunction
        # because all our Groups will reference the files
        # in the FILE section. So we need to know beforehand
        # where those files will be located, while mapping
        # the unique file IDs to the actual offsets written.
        file_chunk_off = info_chunk_off + info_chunk_size
        buffer.write(b'FILE' + b'\x00' * (align_up(0x4, 0x20) - 4))

        file_lookup = {}

        offset = file_chunk_off + 0x20
        for __id, entry in self._file_data._file_data.items():
            file_lookup[__id] = offset

            data = bytes(entry)
            buffer.write(data)
            offset += len(data)

        file_chunk_size = buffer.tell() - info_chunk_size

        # Now write the actual INFO data
        # Write INFO size
        buffer.seek(0x04)
        buffer.write(info_chunk_size.to_bytes(length=4))

        # Write all references
        for off in [snd_tbl_off, bnk_tbl_off, ply_tbl_off, file_tbl_off, grp_tbl_off, arc_info_off]:
            buffer.write(b'\x01\x00\x00\x00' + off.to_bytes(length=4))

        self._write_snd_tbl(buffer)
        self._write_bnk_tbl(buffer)
        self._write_ply_tbl(buffer)
        self._write_file_tbl(buffer)
        self._write_grp_tbl(buffer, file_lookup)
        buffer.write(struct.pack('>HHHHHHH', *self.snd_arc_common_info))

        # Finalize FILE section
        buffer.seek(file_chunk_off - info_chunk_off + 0x4)
        buffer.write(file_chunk_size.to_bytes(length=4, byteorder='big'))

        rsar_buffer.write(buffer.getvalue())
        return info_chunk_off, info_chunk_size, file_chunk_off, file_chunk_size

    @classmethod
    def from_data(cls, data: BinaryIO, file_data: File) -> Self:
        return cls(data, file_data)
