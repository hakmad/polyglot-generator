import pytest

from polyglot_generator import main as pg


class File(pg.file_format.FileFormat):
    """Example file for use in testing.

    Extends pg.file_format.FileFormat.
    """

    def __init__(self, data):
        """Create a new file object."""
        # Initialise the underlying FileFormat.
        pg.file_format.FileFormat.__init__(self, data)

    def host_parasite(self, parasite):
        """Host some parasite dat in the current file.

        Parasites are hosted by inserting them after the first byte.

        Args:
            parasite (bytes): the parasite file to host within the current file.
        """
        polyglot = b""

        # First byte of host file.
        polyglot += self.data[:1]

        # Actual parasite data.
        polyglot += parasite

        # Rest of host data.
        polyglot += self.data[1:]

        return polyglot


class TestStack:
    def test_create_stack_normal(self):
        expected = b"abcdef"

        top = File(b"abc")
        top.supports_stack_after_eof = True

        bottom = File(b"def")
        bottom.supports_stack_before_sof = True

        output = pg.create_stack(top, bottom)

        assert output == expected

    def test_create_stack_no_data_before_sof(self):
        top = File(b"")
        top.supports_stack_after_eof = True

        bottom = File(b"")
        bottom.supports_stack_before_sof = False

        with pytest.raises(pg.StackNotViableException):
            pg.create_stack(top, bottom)

    def test_create_stack_no_data_after_eof(self):
        top = File(b"")
        top.supports_stack_after_eof = False

        bottom = File(b"")
        bottom.supports_stack_before_sof = True

        with pytest.raises(pg.StackNotViableException):
            pg.create_stack(top, bottom)


class TestParasite:
    def test_create_parasite(self):
        expected = b"abcdef"

        host = File(b"aef")
        host.supports_parasite = True
        host.max_parasite_size = 4

        parasite = File(b"bcd")
        parasite.supports_stack_before_sof = True

        output = pg.create_parasite(host, parasite)

        assert output == expected

    def test_create_parasite_no_host_support(self):
        host = File(b"")
        host.supports_parasite = False

        parasite = File(b"")

        with pytest.raises(pg.ParasiteNotViableException):
            pg.create_parasite(host, parasite)

    def test_create_parasite_no_parasite_support(self):
        host = File(b"")
        host.supports_parasite = True
        host.max_parasite_size = 1

        parasite = File(b"")
        parasite.supports_stack_before_sof = False

        with pytest.raises(pg.ParasiteNotViableException):
            pg.create_parasite(host, parasite)

    def test_create_parasite_too_large(self):
        host = File(b"")
        host.supports_parasite = True
        host.max_parasite_size = 1

        parasite = File(b"abc")

        with pytest.raises(pg.ParasiteNotViableException):
            pg.create_parasite(host, parasite)
