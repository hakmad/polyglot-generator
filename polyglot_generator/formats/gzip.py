"""GZIP format.

(Most) GZIP implementations will ignore garbage on the end of the file. As a
result, GZIP files can be used as the top half of a stack file.

As a stack:

+-----------------+
|                 |
|   GZIP file     |   <-- Prepended to the start of the bottom file.
|                 |
+-----------------+
|                 |
|   Bottom file   |
|                 |
+-----------------+
"""


from polyglot_generator.formats import file


class File(file.File):
    """Container for GZIP files.

    Extends file.File.
    """

    def __init__(self, data):
        """Create a new GZIP file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying File.
        file.File.__init__(self, data)

        # Stack options.
        self.supports_stack_after_eof = True
