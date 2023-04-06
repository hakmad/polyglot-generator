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

from polyglot_generator.formats import file


class File(file.File):
    """Container for bottom stack files.

    Extends file.File.
    """

    def __init__(self, data):
        """Create a new file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying File.
        file.File.__init__(self, data)

        # Stack options.
        self.supports_stack_before_sof = True
