import io

from revo_snd.nw4r import *
from revo_snd.rbnk.brbnk import BRBNK
from revo_snd.rseq.brseq import BRSEQ
from revo_snd.rstm.brstm import BRSTM
from revo_snd.rwar.brwar import BRWAR
from revo_snd.rwav.brwav import BRWAV
from revo_snd.rwsd.brwsd import BRWSD


class File:
    __cnt_unique__ = 0

    def __init__(self, data: BinaryIO = None) -> None:
        self._read_files = {}
        self._file_data = {}
        self._id_to_off_map = {}

        self.n_bnk = 0
        self.n_seq = 0
        self.n_strm = 0
        self.n_wav = 0
        self.n_rwar = 0
        self.n_wsd = 0

        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        block_info = read_nw4r_block_header(data)
        block_sanity_check(block_info.magic, 'FILE')

        self._block_size = block_info.block_size
        data.read(24)

        self._read_rsar_files(data)
        data.seek(self._base_offset)

        self.raw_data = data.read(block_info.block_size)

    def _read_rsar_files(self, data: BinaryIO) -> None:
        end_offset = self._base_offset + self._block_size

        offset = data.tell()
        while offset < end_offset:
            magic = data.read(4).decode('ascii')
            data.seek(-4, io.SEEK_CUR)

            origin = data.tell()
            match magic:
                case FileTag.BRBNK:
                    file = BRBNK(data)
                    self._read_files[origin] = File.__cnt_unique__
                    self._file_data[File.__cnt_unique__] = file
                    File.__cnt_unique__ += 1

                    self._increase_type_cnt(file.file_type)
                case FileTag.BRSTM:
                    file = BRSTM(data)
                    self._read_files[origin] = File.__cnt_unique__
                    self._file_data[File.__cnt_unique__] = file
                    File.__cnt_unique__ += 1

                    self._increase_type_cnt(file.file_type)
                case FileTag.BRSEQ:
                    file = BRSEQ(data)
                    self._read_files[origin] = File.__cnt_unique__
                    self._file_data[File.__cnt_unique__] = file
                    File.__cnt_unique__ += 1

                    self._increase_type_cnt(file.file_type)
                case FileTag.BRWAV:
                    file = BRWAV(data)
                    self._read_files[origin] = File.__cnt_unique__
                    self._file_data[File.__cnt_unique__] = file
                    File.__cnt_unique__ += 1

                    self._increase_type_cnt(file.file_type)
                case FileTag.BRWAR:
                    file = BRWAR(data)
                    self._read_files[origin] = File.__cnt_unique__
                    self._file_data[File.__cnt_unique__] = file
                    File.__cnt_unique__ += 1

                    self._increase_type_cnt(file.file_type)
                    self.n_wav += len(file)
                case FileTag.BRWSD:
                    file = BRWSD(data)
                    self._read_files[origin] = File.__cnt_unique__
                    self._file_data[File.__cnt_unique__] = file
                    File.__cnt_unique__ += 1

                    self._increase_type_cnt(file.file_type)
                case _:
                    raise NW4RInvalidFileError(
                        f'Unexpected file type "{magic}" read in BRSAR FILE section at offset 0x{data.tell():X}')

            while data.read(1) == 0:
                pass
            else:
                if data.tell() >= end_offset:
                    break
                data.seek(-1, io.SEEK_CUR)

        self._id_to_off_map = {value: key for key, value in self._read_files.items()}

    def _increase_type_cnt(self, magic: str) -> None:
        match magic:
            case FileTag.BRBNK:
                self.n_bnk += 1
            case FileTag.BRSTM:
                self.n_strm += 1
            case FileTag.BRSEQ:
                self.n_seq += 1
            case FileTag.BRWAV:
                self.n_wav += 1
            case FileTag.BRWAR:
                self.n_rwar += 1
            case FileTag.BRWSD:
                self.n_wsd += 1
            case _:
                raise NW4RInvalidFileError(
                    f'Unexpected file type "{magic}" in FILE section of BRSAR')

    def append(self, file: RevFile) -> int:
        """
        Adds a new file to the FILE block and returns its unique ID.
        Only valid BRSAR files may be added to the FILE block.

        :param file: A valid NW4R file.
        """
        self._increase_type_cnt(file.file_type)

        self._file_data[File.__cnt_unique__] = file
        File.__cnt_unique__ += 1

        return File.__cnt_unique__ - 1

    def offset_to_id(self, offset: int) -> int:
        if offset in self._read_files:
            return self._read_files[offset]

        return -1

    def id_to_offset(self, __id: int) -> int:
        if __id in self._id_to_off_map:
            return self._id_to_off_map[__id]

        return -1

    def __contains__(self, item: int) -> bool:
        return item in self._read_files or item in self._file_data

    def __getitem__(self, item: int):
        if item in self._read_files:
            return self._file_data[self._read_files[item]]
        return self._file_data[item]

    def __bytes__(self) -> bytes:
        buffer = io.BytesIO()
        buffer.write(b'FILE' + b'\x00' * (align_up(0x4, 0x20) - 4))

        for _, entry in self._file_data.items():
            data = bytes(entry)
            buffer.write(data)

        file_chunk_size = buffer.tell()
        buffer.seek(0x4)
        buffer.write(file_chunk_size.to_bytes(length=4, byteorder='big'))

        return buffer.getvalue()
