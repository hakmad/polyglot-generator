"""Polyglot generator library.

Provides functions to create polyglots.
"""


class StackNotViableException(Exception):
    """Raised if a stack is not viable with the two given files/formats."""
    pass


class ParasiteNotViableException(Exception):
    """Raised if a parasite is not viable with the two given files/formats."""
    pass


def create_stack(top, bottom):
    """Create a stack polyglot file.

    Args:
        top (File): top file for the polyglot.
        bottom (File): bottom file for the polyglot.
    """
    if not top.supports_stack_after_eof:
        raise StackNotViableException(f"Top file {top.name} ({top.format}) does
            not support data after EOF!")

    if not bottom.supports_stack_before_sof:
        raise StackNotViableException(f"Bottom file {bottom.name}
            ({bottom.format}) does not support data before EOF!")

    return top.data + bottom.data


def create_parasite(host, parasite):
    """Create a parasite polyglot file.

    Args:
        host (file): host file for the polyglot.
        parasite (file): parasite file for the polyglot.
    """
    if not host.supports_parasite:
        raise ParasiteNotViableException(f"Host file {host.name} 
            ({host.format}) does not support parasites!")

    if not parasite.size > host.max_parasite_size:
        raise ParasiteNotViableException(f"Parasite file {parasite.name}
            ({parasite.format}) exceeds max parasite size for host format
            {host.format}!")

    return host.host_parasite(parasite)
