# subdivision - A tool to help manage your media files
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)\
[![Generic badge](https://img.shields.io/badge/Build-Passing-Green.svg)](https://shields.io/)

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
```
