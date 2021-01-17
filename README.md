# subdivision - A tool to help manage your media files
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)\
[![Generic badge](https://img.shields.io/badge/Build-Passing-Green.svg)](https://shields.io/)\
[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/fold_left.svg?style=social&label=Follow%20%40fold_left)](https://twitter.com/stevezaluk)

A file renaming, formatting, and moving tool with media servers in mind. Works Great with Plex

# Installation

## Requirements
* Python 3
* A Linux or a MacOS computer

## Installation on Linux & Mac
```
git clone https://github.com/zbduid12/subdivision.git
cd subdivision/
chmod +x subdivison3.py
```

# Usage

## Help
```
  subdivision3 - A tool to help manage your media files

    -h : Print this page
    -i : Show info on an item
    -w [directory] : Do a directory walk

  Walk Options:
    --dry-run : Do everything except formatting
    --file-regex [regex] : Use only files that match this regex
    --folder-regex [regex] : Use only directories that match this regex
    --prefix : Set a prefix for your filename. Use --preserve-original-filename to put the original name at the end. Otherwise this will rename it to your prefix
    --preserve-original-filename : Put the original file name in the newly formatted file name
    --topdown : Walk the directory from the top down
    --full-match : Fully match file regex(s) instead of searching for them
```

# Development

## Known Issues
* Initial Directory walk doesnt scan for files in the starting directory
* Calling the prefix argument throws a file not found error and moves the not found file to this directory
* The prefix argument is not perfect lol (needs some work)
* file does not exist error. I believe this is due to the way that the File object scans for metadata

## Future Features
* Full matching instead of searching for regex's during file scan
* Match all regex's present : If a list of regex's is given, match all of them instead of just one
* Suffix options (put text at the end of the filename)
* Center text options (put text at the end of the filename)
* Chmod, Move, and Delete options
*
