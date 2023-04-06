"""Generic top stack file.

Used for experimentation - this file represents the top half of a stack
based polyglot.

As a stack:

+-----------------+
|                 |
|   Top file      |   <-- Prepended to the start of the bottom file.
|                 |
+-----------------+
|                 |
|   Bottom file   |
|                 |
+-----------------+
"""

from polyglot_generator.formats import file


class File(file.File):
    """Container for top stack files.

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
        self.supports_stack_after_eof = True
