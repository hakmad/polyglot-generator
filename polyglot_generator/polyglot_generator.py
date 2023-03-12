#!/usr/bin/env python3

"""Polyglot generator library.

Provides functions to create polyglots.
"""

import argparse


from formats import *


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
        raise StackNotViableException(f"Top file does not support data after EOF!")

    if not bottom.supports_stack_before_sof:
        raise StackNotViableException(f"Bottom file does not support data before EOF!")

    return top.data + bottom.data


def create_parasite(host, parasite):
    """Create a parasite polyglot file.

    Args:
        host (file): host file for the polyglot.
        parasite (file): parasite file for the polyglot.
    """
    if not host.supports_parasite:
        raise ParasiteNotViableException(f"Host file does not support parasites!")

    if not parasite.size < host.max_parasite_size:
        raise ParasiteNotViableException(f"Parasite file exceeds max parasite size for host format!")

    return host.host_parasite(parasite)


def write_to_file(file_name, data):
    """Write some data to a file.

    Args:
        file_name (str): name of file to write.
        data (bytes): byte string to write to file.
    """
    # Open file and write to it.
    with open(file_name, "wb") as file:
        file.write(data)


available_formats = {
    "gif": gif.File,
    "jpeg": jpeg.File,
    "zip": zip.File,
}

available_methods = {
    "stack": create_stack,
    "parasite": create_parasite,
}


def main():
    """Main CLI program."""
    # Setup argument parser.
    parser = argparse.ArgumentParser(
            description="A CLI tool for generating polyglot files")

    # Setup options for argument parser.
    parser.add_argument("-i1", "--input-file-1",
            type=argparse.FileType("rb"), required=True)

    parser.add_argument("-f1", "--file-1-format",
            choices=available_formats.keys(), required=True)

    parser.add_argument("-i2", "--input-file-2",
            type=argparse.FileType("rb"), required=True)

    parser.add_argument("-f2", "--file-2-format",
            choices=available_formats.keys(), required=True)

    parser.add_argument("-m", "--method",
            choices=available_methods.keys(), required=True)

    parser.add_argument("-o", "--output-file",
            default="polyglot")

    # Parse the arguments.
    args = parser.parse_args()
    
    # Get input files.
    input_file_1 = available_formats[args.file_1_format](args.input_file_1.read())
    input_file_2 = available_formats[args.file_2_format](args.input_file_2.read())

    # Process with chosen method.
    polyglot = available_methods[args.method](input_file_1, input_file_2)

    # Write polyglot to file.
    write_to_file(args.output_file, polyglot)


if __name__ == "__main__":
    main()
