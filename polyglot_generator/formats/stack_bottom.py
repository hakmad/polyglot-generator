"""Generic bottom stack file.

Used for experimentation - this file represents the bottom half of a stack
based polyglot.

As a stack:

+-----------------+
|                 |
|   Top file      |
|                 |
+-----------------+
|                 |
|   Bottom file   |   <-- Appended to the end of the top file.
|                 |
+-----------------+
"""

from formats import file_format


class File(file_format.FileFormat):
    """Container for bottom stack files.

    Extends file_format.FileFormat.
    """

    def __init__(self, data):
        """Create a new file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying FileFormat.
        file_format.FileFormat.__init__(self, data)

        # Stack options.
        self.supports_stack_before_sof = True
