import io

from revo_snd.nw4r import *
from revo_snd.rsar.string_trie import StringTrie


class Symbol:
    def __init__(self, data: BinaryIO = None) -> None:
        if data is not None:
            self._load_from_data(data)
        else:
            self.names = []
            self._snd_trie = StringTrie()
            self._ply_trie = StringTrie()
            self._grp_trie = StringTrie()
            self._bnk_trie = StringTrie()

    def _load_from_data(self, data: BinaryIO) -> None:
        base_offset = data.tell()
        block_info = read_nw4r_block_header(data)
        block_sanity_check(block_info.magic, 'SYMB')

        self._base_offset = base_offset
        self._block_size = block_info.block_size

        tbl_off, snd_off, ply_off, grp_off, bnk_off = struct.unpack('>IIIII', data.read(20))

        # Offset to the respective tries
        self._tbl_off = tbl_off + 8 + base_offset
        self._snd_off = snd_off + 8 + base_offset
        self._ply_off = ply_off + 8 + base_offset
        self._grp_off = grp_off + 8 + base_offset
        self._bnk_off = bnk_off + 8 + base_offset

        # Skip the offset table because we don't need it
        str_off_tbl_size = struct.unpack('>I', data.read(4))[0]
        data.seek(data.tell() + (str_off_tbl_size * 4))  # every offset is an u32 value

        self.names = [read_terminated_string(data) for _ in range(str_off_tbl_size)]

        # Load all string tries...
        data.seek(self._snd_off)
        self._snd_trie = StringTrie(data, self.names)

        data.seek(self._ply_off)
        self._ply_trie = StringTrie(data, self.names)

        data.seek(self._grp_off)
        self._grp_trie = StringTrie(data, self.names)

        data.seek(self._bnk_off)
        self._bnk_trie = StringTrie(data, self.names)

    def _assert_unique_name(self, name) -> None:
        if name in self.names:
            raise ValueError('Cannot have multiple same names in the BRSAR!')

    def add_snd(self, name: str, info_idx: int) -> None:
        self._assert_unique_name(name)
        str_idx = len(self.names)

        self.names.append(name)
        self._snd_trie.insert(name, str_idx, info_idx)

    def add_player(self, name: str, info_idx: int) -> None:
        self._assert_unique_name(name)
        str_idx = len(self.names)

        self.names.append(name)
        self._ply_trie.insert(name, str_idx, info_idx)

    def add_group(self, name: str, info_idx: int) -> None:
        self._assert_unique_name(name)
        str_idx = len(self.names)

        self.names.append(name)
        self._grp_trie.insert(name, str_idx, info_idx)

    def add_bank(self, name: str, info_idx: int) -> None:
        self._assert_unique_name(name)
        str_idx = len(self.names)

        self.names.append(name)
        self._bnk_trie.insert(name, str_idx, info_idx)

    def __bytes__(self) -> bytes:
        buffer = io.BytesIO()

        # Write base block header (magic + block_size),
        #       name table offset,
        #       sound trie offset,
        #       player trie offset,
        #       group trie offset,
        #       bank trie offset,
        # all values will be written later.
        buffer.write(b'SYMB' + b'\x00\x00\x00\x00' * 6)

        # Write the offset table
        # The offset table is a table of table consisting of
        #    u32 table_size, elements
        # where all elements in our case are u32 values.
        #
        # We will need exactly as many offsets as we have
        # names, so we know we will have a block with
        #     sizeof(table_size) + (sizeof(u32) * len(self.names))
        #
        # With this information, we can precalculate the offsets
        # for this table. The size of the offset table is written
        # at 0x5C in the BRSAR, and at 0x1C in the SMYB block.
        offset_tbl_offset = buffer.tell() - 0x08
        name_tbl_n_entries = len(self.names)
        name_tbl_start_offset = buffer.tell() + 4 + (4 * name_tbl_n_entries)  # See above explanation

        buffer.write(name_tbl_n_entries.to_bytes(length=4, byteorder='big'))
        offset_to_name = name_tbl_start_offset
        for i in range(name_tbl_n_entries):
            name = self.names[i]

            # - 0x8 to align to the end of the SYMB block header
            # Because when we search for the string we calculate:
            #    SYMB_base_offset + 0x08 + offset
            buffer.write((offset_to_name - 8).to_bytes(length=4, byteorder='big'))
            offset_to_name += len(name) + 1

        # Write strings
        [buffer.write(name.encode('ascii') + b'\x00') for name in self.names]

        # Write sound trie
        snd_trie_offset = buffer.tell() - 0x8
        buffer.write(bytes(self._snd_trie))

        # Write player trie
        ply_trie_offset = buffer.tell() - 0x8
        buffer.write(bytes(self._ply_trie))

        # Write group trie
        grp_trie_offset = buffer.tell() - 0x8
        buffer.write(bytes(self._grp_trie))

        # Write bank trie
        bnk_trie_offset = buffer.tell() - 0x8
        buffer.write(bytes(self._bnk_trie))

        # Finalize SYMB chunk
        buffer.write(b'\x00' * (align_up(buffer.tell(), 0x20) - buffer.tell()))
        data_chunk_size = buffer.tell()

        buffer.seek(0x4)
        buffer.write(struct.pack('>IIIIII', data_chunk_size,
                                 offset_tbl_offset, snd_trie_offset, ply_trie_offset, grp_trie_offset,
                                 bnk_trie_offset))
        return buffer.getvalue()

    @classmethod
    def from_data(cls, data: BinaryIO) -> Self:
        return cls(data)
