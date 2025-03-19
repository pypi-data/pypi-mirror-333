from revo_snd.rseq.mml_parser import MML_Parser
from revo_snd.nw4r import *


class _Version:
    VERSION_1_0 = 0x0100


SUPPORTED_VERSIONS = {_Version.VERSION_1_0}


class _LablEntry:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        self.data_off, self.len_name = struct.unpack('>II', data.read(8))
        self.name = read_string(data, self.len_name)

    def __str__(self) -> str:
        return f'<BRSEQ Label Entry: {self.name}, data_offset=0x{self.data_off:X}>'

    def __repr__(self) -> str:
        return self.__str__()


class _Labl:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        block_info = read_nw4r_block_header(data)
        block_sanity_check(block_info.magic, 'LABL')

        self.n_label, = struct.unpack('>I', data.read(4))
        label_offsets = struct.unpack(f'>{self.n_label}I', data.read(4 * self.n_label))

        self.entries = []
        for off in label_offsets:
            data.seek(self._base_offset + off + 0x08)
            self.entries.append(_LablEntry(data))

        self.entries.sort(key=lambda o: o.data_off)


class _Data:
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_data(data)

    def _read_from_data(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()

        block_info = read_nw4r_block_header(data)
        block_sanity_check(block_info.magic, 'DATA')

        self.data_off = struct.unpack('>I', data.read(4))


class BRSEQ(RevFile):
    def __init__(self, data: BinaryIO) -> None:
        if data is not None:
            self._read_from_file(data)

    def _read_from_file(self, data: BinaryIO) -> None:
        self._base_offset = data.tell()
        self.base_offset = self._base_offset

        self.file_info = read_nw4r_file_header(data)
        file_sanity_check(self.file_info.magic, self.file_info.byte_order, self.file_info.version, FileTag.BRSEQ, SUPPORTED_VERSIONS)
        self._file_size = self.file_info.file_size

        self.data_off, self.data_size, self.label_off, self.label_size = struct.unpack('>IIII', data.read(16))

        data.seek(self._base_offset + self.label_off)
        self.label_off += self._base_offset
        self._label = _Labl(data)

        data.seek(self._base_offset + self.data_off)
        self.data_off += self._base_offset
        self._data = _Data(data)

        # call parser and decode this shit
        self._mml_parser = MML_Parser(data, self._label.entries, (self.data_off + 0xC))

        self._seq_data = self._mml_parser.parse()

        data.seek(self._base_offset)
        self.raw_data = data.read(self.file_info.file_size)

        # Restore state to the expected position of the reader
        data.seek(self._base_offset + self.file_info.file_size)

    def __bytes__(self) -> bytes:
        return self.raw_data

    def __contains__(self, item) -> bool:
        try:
            self.__getitem__(item)
            return True
        except IndexError:
            return False

    def __getitem__(self, key):
        # We either find entries by:
        #   1. their name               (named labels only)
        #   2. their relative offset    (named labels and anonymous labels)
        #   3. their absolute offset    (named labels and anonymous labels)
        if isinstance(key, int):
            _data_off = self.data_off + 0xC

            __item = self._seq_data.get(key, None)  # relative offset of anonymous label
            __item_2 = self._seq_data.get(key - _data_off, None)  # absolute offset of anonymous label

            # If we didn't find anything at this point, this means we
            # do not have an anonymous label but a named label, so we
            # need to search manually for that
            if __item is None and __item_2 is None:
                for seq in self._seq_data.values():
                    if seq.label is not None and (((key + _data_off) == (seq.label.data_off + _data_off))
                                                  or key == (seq.label.data_off + _data_off)):
                        return seq
                raise IndexError(f'Unknown BRSEQ entry {key}')

            return __item_2 if __item is None else __item

        elif isinstance(key, str):
            __item = self._seq_data.get(key, None)
            if __item is None:
                raise IndexError(f'Unknown BRSEQ entry {key}')

            return __item

        raise IndexError(f'Unsupported key type "{type(key)}" with value "{key}" for BRSEQ')

    @classmethod
    def from_file(cls, data: (str | BinaryIO), *args, **kwargs) -> Self:
        return cls(open(data, 'rb')) if isinstance(data, str) else cls(data)
