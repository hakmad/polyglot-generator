"""ZIP format.

(Most) ZIP implementations support data before the start of file marker (PK
followed by 0x03 0x04 in little-endian format) and after the end of file (it
doesn't technically have an EOF marker, but it stops parsing when it finds the
end of central directory record). As a result, ZIP can be used as the bottom
half of a stack file or as a parasite within the host file.

As a stack:

+--------------+
|              |
|   Top file   |
|              |
+--------------+
|              |
|   ZIP file   |   <-- Appended to the end of the top file.
|              |
+--------------+

As a parasite:

+---------------+
|               |
|   Host file   |
|               |
+---------------+
|               |
|   ZIP file    |   <-- As a comment/ignored section within the host file.
|               |
+---------------+
|               |
|   Host file   |
|               |
+---------------+

Care should be taken to ensure that the ZIP file actually fits into the
comment/ignored section of a host - large ZIP files may not work.
"""

import formats


class File(formats.File):
    """Container for ZIP files.

    Extends formats.File.
    """

    def __init__(self, data):
        """Create a new ZIP File object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying File.
        formats.File.__init__(self, data)

        # Stack options.
        self.supports_stack_before_sof = True
        self.supports_stack_after_eof = True
