"""BZIP2 format.

(Most) BZIP2 implementations will ignore garbage on the end of the file. As a
result, BZIP2 files can be used as the top half of a stack file.

As a stack:

+-----------------+
|                 |
|   BZIP2 file    |   <-- Prepended to the start of the bottom file.
|                 |
+-----------------+
|                 |
|   Bottom file   |
|                 |
+-----------------+
"""


from polyglot_generator.formats import file

class File(file.File):
    """Container for BZIP2 files.

    Extends file.File.
    """

    def __init__(self, data):
        """Create a new BZIP2 file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying File.
        file.File.__init__(self, data)

        # Stack options.
        self.supports_stack_after_eof = True
