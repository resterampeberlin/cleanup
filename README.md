[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Issues](https://img.shields.io/github/issues/resterampeberlin/cleanup)](https://github.com/resterampeberlin/cleanup/issues)
[![Tags](https://img.shields.io/github/v/tag/resterampeberlin/cleanup)](https://github.com/resterampeberlin/cleanup/tags)
[![Release](https://img.shields.io/github/v/release/resterampeberlin/cleanup)](https://github.com/resterampeberlin/cleanup.git)
[![Downloads](https://img.shields.io/github/downloads/resterampeberlin/cleanup/total)](https://github.com/resterampeberlin/cleanup.git)
              
# Purpose

This script clean files produced by Apple iCLoud synchronisation. Those have usually the name `file 2`, `.file 2`, or `file 2.icloud`. The original filenames are "`file` or `.file`.

The script find those files, checks if a original file is present in the same directory and deletes or simply shows the filenames. 
The script searches in a given subdirectory and all its subfolders.

# Command line options

## Help (-h, --help)

Show a help text

## Dry run (--dry-run)

Show only the duplicate files. The script does not delete any file. 
The default is to show duplicate files.

## Force (--force)

Usually the script asks before deleting a file. With `--force` the file is deleted immediately. 
The default is to aks before deleting.

`--dry-run` and `--force`are mutually exclusice.

## Don´t show valid file (--no-valid)

You may have valid files named `file 2`. Usually the script show those when there is **no** `file` in the same directory. Use `--no-valid` to suppress this message. 
The default is to show valid files also.

## Pathname

Start the scan in that path. 
The default is `.`

# Suppress analysis for certain directories

Generate an empty `.nocleanup` file if you want to suppress any action (printing, deleting) for an individual directory

# Examples

        cleanup.py 

Runs in current directory, show all duplicates and ask before deleting any files

        cleanup.py --dry-run .

Runs in current directory, do not delete, show valid files also

        cleanup.py --force Documents

Delete all duplicates in `Documents`

        cleanup.py --dry-run --no-valid Projects

Show only duplicates in `Proejcts` directory and subdirectories.

# Credits

This open source code project is has been proudfully produced in Berlin (and other places around the globe) by

![Logo](img/Logo180x180.png)

