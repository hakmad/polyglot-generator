"""Formats module.

This module contains a template File class that can be extended for different
formats.
"""

__all__ = [
    "zip",
]


class File:
    """Container class for other formats.

    Designed to be extended to other formats.

    Attributes:
        name (str): name of the file.
        formats (str): format of the file.
        data (bytes): data of the file.
        size (int): size (in bytes) of the file.

        supports_stack_before_sof (bool): does the format support data before
            the start of file marker?
        supports_stack_after_eof (bool): does the format support data after the
            end of file marker?

        supports_parasite (bool): does the format support parasite data
            structures?
        max_parasite_size (int): maximum size for a parasite.
    """

    def __init__(self, name, format):
        """Create a new File object.

        Args:
            name (str): name of the file.
            format (str): format of the file.
        """
        # Metadata.
        self.name = name
        self.format = format

        # Actual data.
        with open(self.name, "rb") as file:
            self.data = file.read()

        self.size = len(self.data)

        # Stack options.
        self.supports_stack_before_sof = False
        self.supports_stack_after_eof = False

        # Parasite options.
        self.supports_parasite = False
        self.max_parasite_size = 0

    def host_parasite(self, parasite):
        """Host a parasite in the current file.

        This method is intended to be called from the host file.

        This method is intended to be overridden by any classes that extend
        this format (given that the format supports creating parasites).

        Args:
            parasite (File): the parasite file to host within the current file.

        Examples:
            host = File(...)
            parasite = File(...)
            ...
            polyglot = host.host_parasite(parasite)
        """
        pass
