"""ELF format.

The ELF format uses offsets to specify where different segments and sections
start. Data placed after all sections and segments in the ELF file is not
interpreted by the interpreter, and as a result ELF can be used as the top half
of a stack file.

As a stack:

+-----------------+
|                 |
|   ELF file      |   <--- Prepended to the start of the bottom file.
|                 |
+-----------------+
|                 |
|   Bottom file   |
|                 |
+-----------------+
"""


from formats import file_format


class File(file_format.FileFormat):
    """Container for GIF files.

    Extends file_format.FileFormat.
    """

    def __init__(self, data):
        """Create a new GIF file object.

        Args:
            data (bytes): byte string containing the contents of the file.
        """
        # Initialise the underlying FileFormat.
        file_format.FileFormat.__init__(self, data)

        # Stack options.
        self.supports_stack_after_eof = True
