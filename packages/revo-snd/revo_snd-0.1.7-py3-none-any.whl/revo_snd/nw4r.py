import dataclasses
import enum
import math
import os
import struct
from collections import namedtuple
from typing import BinaryIO, Self

from revo_snd.nw4r_err import *

NW4R_LIB_VERSION = '0.1.1'


class FileTag(enum.StrEnum):
    BRSAR = "RSAR"
    BRSEQ = "RSEQ"
    BRWAR = "RWAR"
    BRWAV = "RWAV"
    BRBNK = "RBNK"
    BRSTM = "RSTM"
    BRWSD = "RWSD"


class ByteOrder(enum.IntEnum):
    BIG_ENDIAN = 0xFEFF
    LITTLE_ENDIAN = 0xFFFE


class RefType(enum.IntEnum):
    ABSOLUTE = 0
    RELATIVE = 1


Reference = namedtuple('Reference', ['flag', 'data_type', 'offset'])
NW4R_SIZE_OF_REFERENCE = 8
NW4R_EMPTY_REFERENCE = b'\x00' * NW4R_SIZE_OF_REFERENCE

# Class for subsections inside a file
RevBlock = namedtuple('RevBlock', ['magic', 'block_size'])


def NW4R_BUILD_BYTES_FOR_REF(offset: int, *, ref_type: RefType = RefType.RELATIVE, data_type: int = 0) -> bytes:
    """
    Returns the specified data for an NW4R Reference (as defined in the Reference class)
    as a bytes-like object.

    :param offset:     The target offset.
    :param ref_type:   (Optional) Type of the reference. Default value = 1 (RELATIVE OFFSET).
    :param data_type:  (Optional) Data type used by the reference. Default value = 0.
    """
    RefType(ref_type)  # Check if this is a valid ref type
    return struct.pack('>BBHI', ref_type, data_type, 0, offset)


def align_up(val: (float | int), alignment: int) -> int:
    """
    Aligns the given value by the given alignment.
    :param val:       The value to align.
    :param alignment: The alignment to use for the value.
    """
    return math.ceil(val / alignment) * alignment


def int_align(value: int, align: int) -> int:
    """
    Aligns an integer value by the given alignment.
    :param value: The value to align.
    :param align: The alignment to use for the value.
    """
    return value if align <= 0 else (value + align - 1) // align * align


def round_up(x: int, base: int) -> int:
    """
    Rounds x up to a multiple of base.
    :param x:    The value to round up.
    :param base: The base to use to round up the value.
                 Must be a multiple of 2.
    """
    return (x + (base - 1)) & ~(base - 1)


def print_warning(message: str) -> None:
    """
    Prints a warning to the standard output stream.
    :param message: The message to display.
    """
    print(f"{'\033[93m'}{message}{'\033[0m'}")


@dataclasses.dataclass
class RevFileInfo:
    magic: str
    byte_order: int
    version: int
    file_size: int
    header_size: int
    n_section: int

    def __str__(self) -> str:
        return (f'<RevFile({self.magic}, byte_order=0x{self.byte_order:X},'
                f' version=0x{self.version:X}, file_size={self.file_size}, header_size={self.header_size},'
                f' n_section={self.n_section})')

    def __repr__(self) -> str:
        return self.__str__()


class RevFile:
    base_offset: int = -1
    file_info: RevFileInfo = None

    @property
    def file_type(self) -> str:
        return self.file_info.magic

    @property
    def byte_order(self) -> str:
        if self.file_info.byte_order == ByteOrder.BIG_ENDIAN:
            return 'big_endian'
        elif self.file_info.byte_order == ByteOrder.LITTLE_ENDIAN:
            return 'little_endian'
        else:
            return '<UNKNOWN BYTE_ORDER>'

    @property
    def size(self) -> int:
        return self.file_info.file_size

    @property
    def n_sections(self) -> int:
        return self.file_info.n_section

    @property
    def header_size(self) -> int:
        return self.file_info.header_size

    @property
    def version(self) -> str:
        version_value = self.file_info.version
        return str(version_value >> 8) + '.' + str(version_value & 0x00FF)

    @classmethod
    def from_file(cls, data: (str | BinaryIO), *args, **kwargs) -> Self:
        """
        Loads this Nintendo Revolution file from the given file buffer
        OR the given file path and returns this file, initiated with all data.
        """
        raise NotImplementedError


def block_sanity_check(magic: str, expected_magic: str) -> None:
    if magic != expected_magic:
        raise AssertionError(f'Expected to read a "{expected_magic}" block but read "{magic}" instead')


def file_sanity_check(magic: str, byte_order: int, version: int, expected_magic: str,
                      expected_versions: set[int]) -> None:
    if magic != expected_magic:
        raise NW4RInvalidFileError(f'Expected to read a B{expected_magic} file but read a B{magic} file instead')

    if version not in expected_versions:
        raise NW4RVersionError(f'The file version {str(version >> 8) + '.' + str(version & 0x00FF)}'
                               f' is not supported for B{magic} files')

    if byte_order != ByteOrder.BIG_ENDIAN:
        raise NW4RByteOrderError('Can only read Nintendo Ware files in big endian byte order')


def read_nw4r_file_header(data: BinaryIO) -> RevFileInfo:
    """
    Common structure for NW4R file headers:
        u32 magic       - magic word for the file
        u32 byte_order  - the byte order of the file (always big_endian == 0xFEFF)
        u32 version     - version of the file
        u32 file_size   - total size of the file in bytes
        u16 header_size - total size of the header in bytes
        u16 n_section   - number of subsections/blocks inside this file
    Reads the header for a NW4R file and returns a named tuple RevFileInfo with
    (magic, byte_order, version, file_size, header_size, n_section). A file may
    have additional data after the base header which is not being read by this function.
    """
    magic, byte_order, version, file_size, header_size, n_section = struct.unpack('>4sHHIHH', data.read(16))

    return RevFileInfo(magic.decode('ascii'), byte_order, version, file_size, header_size, n_section)


def read_nw4r_block_header(data: BinaryIO) -> RevBlock:
    """
    Common structure for NW4R file blocks:
        u32 magic      - magic word for the block
        u32 block_size - total size of the block
    Reads the header for a NW4R block and returns a named tuple RevBlock with (magic, block_size). A block may
    have additional data after the base header which is not being read by this function.
    """
    magic, block_size = struct.unpack('>4sI', data.read(8))
    return RevBlock(magic.decode('ascii'), block_size)


def read_nw4r_ref(data: BinaryIO) -> Reference | None:
    """
    Common structure for NW4R references:
        u8 (bool) byte flag - whether the reference is relative to the (start of the block + 8) containing this reference
                              or if the reference points directly at the specified address
        u8 byte data type   - references are defined as template structures holding a maximum of 4 different possible
                              datatypes a reference can point at with at least one type being mandatory to be specified
                              (template<typename T, typename t1=void, typename t2=void, typename t3=void>). So this
                              field references the index number of the four given types (0, 1, 2, 3). Most of the time,
                              this field is 0.
        2 byte padding
        u32 offset          - the actual offset this reference points to in accordance to the byte flag (see above).

    This function will read such a reference and return a named tuple (see Reference) containing the fields
    flag, data_type and offset. If the reference is a NULL reference, then None is returned.
    """

    flag, data_type, _, offset = struct.unpack('>BBHI', data.read(8))
    if flag == 0 and data_type == 0 and offset == 0:
        return None

    return Reference(flag, data_type, offset)


def get_offset_from_ref(ref: Reference, base_offset: int) -> int:
    """
    See read_nw4r_ref() for an explanation of the Reference structure.
    Reads the exact offset of a Reference object returned by read_nw4r_ref().
    """
    return base_offset + 0x08 + ref.offset if ref.flag == RefType.RELATIVE else ref.offset


def read_offset_from_ref(data: BinaryIO, base_offset: int) -> int:
    """
    See read_nw4r_ref for an explanation of the Reference structure.
    Reads a Reference from the given data and returns the exact offset
    it is pointing at.
    """
    ref = read_nw4r_ref(data)
    if ref is None:
        return -1

    return base_offset + 8 + ref.offset if ref.flag == RefType.RELATIVE else ref.offset


def read_terminated_string(data: BinaryIO, __format: str = 'ascii') -> str:
    """
    Reads a null terminated string from the given buffer.
    :param data:     The buffer to read the data from.
    :param __format: (Optional) The format of the string to read (ascii, utf-8, ...). Default is 'ascii'.
    :return: The read string.
    """
    string_bytes = b''
    while True:
        char_byte = data.read(1)
        if not char_byte or char_byte == b'\x00':
            break
        string_bytes += char_byte
    return string_bytes.decode(__format)


def read_string(data: BinaryIO, __len: int, __format: str = 'ascii') -> str:
    """
    Reads a string from the given buffer with the length of it being predetermined
    by the __len value.

    :param data:     The buffer to read the data from.
    :param __len:    The length of the string.
    :param __format: (Optional) The format of the string to read (ascii, utf-8, ...). Default is 'ascii'.
    :return: The read string of length __len.
    """
    return struct.unpack(f'>{__len}s', data.read(__len))[0].decode(__format)
