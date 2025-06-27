#!/usr/bin/env python3

import sys
import argparse


class SetAllOptions(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, "show_ends", True)
        setattr(namespace, "show_tabs", True)
        setattr(namespace, "show_nonprinting", True)


parser = argparse.ArgumentParser(prog="cat", description="Concatenate FILE(s) to standard output.\n\nWith no FILE or when FILE is -, read standard input.")
parser.add_argument("files", metavar="FILE", type=str, nargs="*", help="A file to print or - for standard input")
parser.add_argument("-A", "--show-all", action=SetAllOptions, help="equivalent to -vET")
parser.add_argument("-E", "--show-ends", action="store_true", help="display $ at the end of each line")
parser.add_argument("-T", "--show-tabs", action="store_true", help="display TAB character as ^I")
parser.add_argument("-v", "--show-nonprinting", action="store_true", help="use ^ and M- notation, except for LFD and TAB")


def get_replacements(
    show_ends: bool, show_tabs: bool, show_nonprinting: bool
) -> dict[int, str]:
    replacements: dict[int, str] = {}

    if show_ends:
        replacements[10] = "$\n"

    if show_tabs:
        replacements[9] = "^I"

    if show_nonprinting:
        for i in range(9):
            replacements[i] = "^" + chr(i + 64)
        for i in range(11, 32):
            replacements[i] = "^" + chr(i + 64)
        for i in range(128, 160):
            replacements[i] = "M-^" + chr(i - 64)
        for i in range(160, 255):
            replacements[i] = "M-" + chr(i - 128)
        replacements[255] = "M-^?"
    
    return replacements

def display_data(data: str, replacements: dict[int, str]):
    output = ""
    for c in data:
        if ord(c) in replacements:
            output += replacements[ord(c)]
        else:
            output += c
    sys.stdout.write(output)

def display_binary_data(data: bytes, replacements: dict[int, str]):
    output = ""
    for c in data:
        if c in replacements:
            output += replacements[c]
        else:
            output += chr(c)
    sys.stdout.write(output)

def cat_from_stdin(replacements: dict[int, str]):
    try:
        while True:
            c = sys.stdin.read(1)
            if c == "":
                break
            display_data(c + sys.stdin.readline(), replacements)
    except KeyboardInterrupt:
        sys.exit(0)
    except EOFError:
        pass

def main():
    args = parser.parse_args()
    replacements = get_replacements(
        args.show_ends, args.show_tabs, args.show_nonprinting
    )

    if len(args.files) == 0:
        cat_from_stdin(replacements)

    for filename in args.files:
        if filename == "-":
            cat_from_stdin(replacements)
            continue

        try:
            with open(filename, "rb") as f:
                display_binary_data(f.read(), replacements)
        except FileNotFoundError:
            print("cat: %s: No such file or directory" % filename, file=sys.stderr)
        except IsADirectoryError:
            print("cat: %s: Is a directory" % filename, file=sys.stderr)

if __name__ == "__main__":
    main()
