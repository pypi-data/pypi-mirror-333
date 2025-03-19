"""
Top-level module containing all error types.
Included in nw4r.py so no need to include this
module separately.
"""


class NW4RInternalError(Exception):
    """
    Indicates an error in the internal API occurred.
    """
    pass


class NW4RInvalidFileError(Exception):
    """
    Indicates that an invalid or unexpected file or file data
    was read.
    """
    pass


class NW4RVersionError(Exception):
    """
    Indicates an invalid version for a NW4R file.
    """
    pass


class NW4RByteOrderError(Exception):
    """
    Indicates an invalid byte order for a NW4R file.
    """
    pass
