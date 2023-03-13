"""JPEG format.

JPEG implementations usually ignore data after the JPEG EOI marker (FF D9 in
big endian format). They also do not enforce any specific format for comments,
only limiting the size of comments to 65533 bytes (the size of a comment is
stored in 2 bytes, but includes the size of the comment itself). As a result,
JPEG can be used as the top half of a stack file or as the host file for a
parasite.

As a stack:

+-----------------+
|                 |
|   JPEG file     |   <-- Prepended to the top of the bottom file.
|                 |
+-----------------+
|                 |
|   Bottom file   |
|                 |
+-----------------+

As a host:

+-----------------------------+
|                             |
|   JPEG SOI (FF D8)          |   <--+
|                             |      |
+-----------------------------+      |
|                             |      |
|   JPEG comment (FF FE)      |   <--+
|                             |      |
+-----------------------------+      |-- JPEG header section.
|                             |      |
|   Parasite size (2 bytes)   |   <--+
|                             |      |
+-----------------------------+      |
|                             |      |
|   Parasite file             |   <--+
|                             |
+-----------------------------+
|                             |
|   Rest of JPEG file         |   <-- Actual JPEG data.
|                             |
+-----------------------------+

Care should be taken to ensure that parasite data fits within the JPEG comment
section.
"""


import formats


class File(formats.File):
    """Container for JPEG files.

    Extends formats.File.
    """

    def __init__(self, data):
        """Create a new JPEG file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying File.
        formats.File.__init__(self, data)

        # Stack options.
        self.supports_stack_after_eof = True

        # Parasite options.
        self.supports_parasite = True
        self.max_parasite_size = 0xFFFF - 2

    def host_parasite(self, parasite):
        """Host some parasite data in the current file.

        Parasites are hosted by inserting a comment right after the JPEG SOI
        marker.

        Args:
            parasite (bytes): the parasite file to host within the current file.
        """
        polyglot = b""

        # Magic bytes of host JPEG file.
        polyglot += self.data[:2]

        # JPEG comment marker with parasite length.
        polyglot += b"\xFF\xFE"
        polyglot += (len(parasite) + 2).to_bytes(2, "big")

        # Actual parasite data.
        polyglot += parasite 

        # Rest of host data.
        polyglot += self.data[2:]

        return polyglot
