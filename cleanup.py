#! /opt/homebrew/bin/python3

import sys
import os
from os.path import join
import re
from termcolor import colored
import glob
import argparse
import click

# some statistics
duplicates = 0
noDuplicates = 0
deleted = 0

# matches all valid filenames
pattern = r"([\(\)\/\.\+\$\-\w\W]+)"


def find(filePattern, namePattern):
    global duplicates
    global noDuplicates
    global deleted

    for duplicate in glob.glob(join(sourcePath, filePattern), recursive=True):
        currentDir = os.path.dirname(duplicate)

        # do not do anything if this file is present in the directory
        if not os.path.isfile(join(currentDir, ".nocleanup")):
            p = re.compile(namePattern, re.IGNORECASE)
            match = p.match(duplicate)

            if match:
                if len(match.groups()) == 2:
                    original = match.group(1) + "." + match.group(2)
                else:
                    original = match.group(1)

                if os.path.isfile(original):
                    duplicates += 1

                    if args.dry_run:
                        print("found " + colored(duplicate, "red") + " = " + original)
                    else:
                        if args.force or click.confirm(
                            "Delete " + colored(duplicate, "red") + " = " + original,
                            default=True,
                        ):
                            deleted += 1

                            os.remove(duplicate)
                else:
                    noDuplicates += 1

                    if not args.no_valid:
                        print("valid file" + colored(duplicate, "green"))
            else:
                # that means, that match could not find the required pattern
                # that could be a very weird filename for example with strange characters
                print("no match " + colored(duplicate, "yellow"))


# Create the command line parser
parser = argparse.ArgumentParser(
    description="Cleanup duplicates from icloud",
    epilog='Default is to ask before deleting a file. Place an empty ".nocleanup" file in directories you don`t want to analyse.',
)

# don´t allow both of below arguments
feature_parser = parser.add_mutually_exclusive_group(required=False)
feature_parser.add_argument(
    "--dry-run",
    default=False,
    action="store_true",
    help="do not delete, show only analysis",
)
feature_parser.add_argument(
    "--force", default=False, action="store_true", help="don't ask before deleting"
)

parser.add_argument(
    "--no-valid",
    default=False,
    action="store_true",
    help="don't show valid files, show only duplicates",
)

parser.add_argument(
    "path",
    default=".",
    type=str,
    nargs="?",
    help="path to start scanning. Default is .",
)

# parse command line
args = parser.parse_args()

# use ** for recursion
sourcePath = join(args.path, "**")

print("Looking for duplicates in " + args.path)

# find "duplicate 2.x"
find("* 2.*", "^" + pattern + " 2\." + pattern + "$")

# find "duplicate 2"
find("* 2", "^" + pattern + " 2$")

# find ".duplicate 2.pdf"
find(".* 2.*", "^" + pattern + " 2\." + pattern + "$")

# find ".duplicate 2"
find(".* 2", "^" + pattern + " 2$")

print(
    "Found "
    + colored(str(noDuplicates), "green")
    + " valid files, "
    + colored(str(duplicates), "red")
    + " duplicates, deleted "
    + str(deleted)
    + " duplicates"
)

exit(1)
