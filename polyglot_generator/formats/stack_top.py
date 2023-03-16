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

import formats


class File(formats.File):
    """Container for top stack files.

    Extends formats.File.
    """

    def __init__(self, data):
        """Create a new file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying File.
        formats.File.__init__(self, data)

        # Stack options.
        self.supports_stack_after_eof = True
