"""7ZIP format.

(Most) 7ZIP implementations support data before the start of file marker (7Z
followed by 0xBC 0xAF 0x27 0x1C in big-endian format) and after the end of file
(it doesn't technically have an EOF marker, but it stops parsing when it finds
the end of the 7ZIP file). As a result, 7ZIP can be used as the bottom half of
a stack file or as a parasite within the host file.

As a stack:

+---------------+
|               |
|   Top file    |
|               |
+---------------+
|               |
|   7ZIP file   |   <-- Appended to the end of the top file.
|               |
+---------------+

As a parasite:

+---------------+
|               |
|   Host file   |
|               |
+---------------+
|               |
|   7ZIP file   |   <-- As a comment/ignored section within the host file.
|               |
+---------------+
|               |
|   Host file   |
|               |
+---------------+

Care should be taken to ensure that the 7ZIP file actually fits into the
comment/ignored section of a host - large 7ZIP files may not work.
"""

from polyglot_generator.formats import file


class File(file.File):
    """Container for 7ZIP files.

    Extends file.File.
    """

    def __init__(self, data):
        """Create a new 7ZIP file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying File.
        file.File.__init__(self, data)

        # Stack options.
        self.supports_stack_before_sof = True
        self.supports_stack_after_eof = True
