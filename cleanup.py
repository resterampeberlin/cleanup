#! /usr/bin/python3

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

# search pattern
pattern = re.compile("^.*\\/(.*)( [0-9]+)(\\..*)?$", re.IGNORECASE)

# process one file, check if duplicate exists
def processFile(currentFile):
    global duplicates
    global noDuplicates
    global deleted
    global pattern

    match = pattern.match(currentFile)

    if match:
        if match.group(3) != None:
            original = join(os.path.dirname(currentFile),match.group(1) + match.group(3))
        else:
            original = join(os.path.dirname(currentFile),match.group(1))

        if os.path.isfile(original):
            duplicates += 1

            if args.dry_run:
                if not args.only_valid:
                    print("found " + colored(currentFile, "red") + " = " + original)
            else:
                if args.force or click.confirm(
                    "Delete " + colored(currentFile, "red") + " = " + original,
                    default=True,
                ):
                    deleted += 1

                    os.remove(currentFile)
        else:
            noDuplicates += 1

            if not args.no_valid:
                print("valid file " + colored(currentFile, "green"))


# process one directory
def processPath(currentPath):
     # do not do anything if this file is present in the directory
    if os.path.isfile(join(path, ".nocleanup")):  
        print("Skipping " + colored(path, "green"))
    else:
        # iterate over all files
        for file in glob.glob(join(currentPath,"*")):
            processFile(file)

        for file in glob.glob(join(currentPath,".*")):
            processFile(file)
        

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
    "--only-valid",
    default=False,
    action="store_true",
    help="don't show duplicates, show only valid files",
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
sourcePath = join(args.path, "**/")

print("Looking for duplicates in " + args.path)

# iterate over all directories
for path in glob.glob(sourcePath, recursive=True):
    try:
        processPath(path)
    except click.exceptions.Abort:
        print ("Aborted")
        break

# print statistics    
print(
    "Found "
    + colored(str(noDuplicates), "green")
    + " valid file(s), "
    + colored(str(duplicates), "red")
    + " duplicate(s), deleted "
    + colored(str(deleted), "red")
    + " duplicate(s)"
)

exit(1)
