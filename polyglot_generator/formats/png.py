"""PNG format.

PNG implementations usually ignore data after the PNG IEND marker. They enforce
a specific format for comments (iTXt requires UTF-8 text, tEXt requires
ISO/IEC 8859-1) however, ad hoc comments can be created which may be ignored by
the parser. The maximum size of comments (and chunks in general) is 4294967295
bytes (the size of a chunk is specified by 4 bytes). As a result, PNG can be
used as the top half of a stack file or as the host file for a parasite.

As a stack:

+-----------------+
|                 |
|   PNG file      |   <-- Prepended to the top of the bottom file.
|                 |
+-----------------+
|                 |
|   Bottom file   |
|                 |
+-----------------+

As a host:

+------------------------------+
|                              |
|   PNG header marker          |   <--+
|                              |      |
+------------------------------+      |-- PNG header section.
|                              |      |
|   PNG IHDR chunk             |   <--+
|                              | 
+------------------------------+
|                              |
|   Parasite file size         |   <--+
|                              |      |
+------------------------------+      |
|                              |      |
|   PNG comment chunk marker   |   <--+
|                              |      |
+------------------------------+      |-- Parasite section.
|                              |      |
|   Parasite file              |   <--+
|                              |      |
+------------------------------+      |
|                              |      |
|   CRC checksum for chunk     |   <--+
|                              |
+------------------------------+
|                              |
|   Rest of PNG file           |   <-- Actual PNG data.
|                              |
+------------------------------+

Care should be taken to ensure that parasite data fits within the PNG comment
section, and to ensure that the CRC checksum is calculated correctly for the
file.
"""


import binascii
import formats


class File(formats.File):
    """Container for PNG files.

    Extends formats.File.
    """

    def __init__(self, data):
        """Create a new PNG file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying File.
        formats.File.__init__(self, data)

        # Stack options.
        self.supports_stack_after_eof = True

        # Parasite options.
        self.supports_parasite = True
        self.max_parasite_size = 0xFFFFFFFF

    def host_parasite(self, parasite):
        """Host some parasite data in the current file.

        Parasites are hosted by inserting a comment right after the PNG IHDR
        chunk.

        Args:
            parasite (bytes): the parasite file to host within the current file.
        """
        polyglot = b""

        # Magic bytes and IHDR chunk of host PNG file.
        polyglot += self.data[:33]

        # Parasite size.
        polyglot += (len(parasite)).to_bytes(4, "big")

        # PNG comment marker.
        polyglot += b"cOMM" 

        # Actual parasite data.
        polyglot += parasite

        # PNG CRC checksum.
        polyglot += binascii.crc32(b"cOMM" + parasite).to_bytes(4, "big")

        # Rest of host data.
        polyglot += self.data[33:]

        return polyglot
