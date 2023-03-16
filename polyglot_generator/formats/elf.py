"""GIF format.

(Most) GIF implementations do not parse beyond the image/file terminator marker (00
3B in big endian format). Data placed after this marker is ignored by the GIF
parser and as a result GIF can be used as the top half of a stack file. 

As a stack:

+-----------------+
|                 |
|   GIF file      |   <-- Prepended to the start of the bottom file.
|                 |
+-----------------+
|                 |
|   Bottom file   |
|                 |
+-----------------+

GIF89a contains a mechanism for creating comments, however these are limited to
255 bytes in length. The GIF file format also expects the file header to be at
offset 0, and as a result parasite based polyglots are generally not possible
(except for very small files with GIF as the host).
"""


import formats


class File(formats.File):
    """Container for GIF files.

    Extends formats.File.
    """

    def __init__(self, data):
        """Create a new GIF file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying File.
        formats.File.__init__(self, data)

        # Stack options.
        self.supports_stack_after_eof = True
