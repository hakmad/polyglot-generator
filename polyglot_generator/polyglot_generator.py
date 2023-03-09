"""Polyglot generator library.

Provides functions to create polyglots.
"""


def create_stack(top, bottom):
    """Create a stack polyglot file.

    Args:
        top (File): top file for the polyglot.
        bottom (File): bottom file for the polyglot.
    """
    return top.data + bottom.data


def create_parasite(host, parasite):
    """Create a parasite polyglot file.

    Args:
        host (file): host file for the polyglot.
        parasite (file): parasite file for the polyglot.
    """
    return host.host_parasite(parasite)
