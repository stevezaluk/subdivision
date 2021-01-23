#!/usr/bin/env python3
import os, sys, argparse
sys.path.insert(1, '/Users/szaluk/lab/projects/vault_suite/subdivision')
from sprint.walk import Walk
from sprint.options import WalkOptions
from sprint.file import File

# Known Issues:
# Some times while scanning for files sprint throws a FileNotFoundError due to incorrect path parsing
# ^ Top Priority

# Initial directory walk doesnt scan for files in the starting directory

# Calling the prefix argument throws a file not found error and moves the not found file to this directory
# The prefix argument is not perfect lol (needs some work)

# file and folder regex issues from argparse
# file does not exist error. I believe this is due to the way that the File object scans for metadata

# Future Features:
# full matching (done)
# match all regex's present : Match all regular expressions in a list (if one is present) instead of just one
# suffix options
# center text option
# chmod, move, delete options
# extension discrimination

# add manual counting
# add way to verify that files have been renamed properly


def usage():
    print('')
    print(' subdivision3 - Helps manage your media server')
    print('')
    print('     -h : Show this page')
    print('     -i : Show info on an item')
    print('     -w [directory] : Do a directory walk')
    print('')
    print(' Walk Options: ')
    print('     --dry-run : Do everything except formatting')
    print('     --file-regex [regex] : Use only files that match the regex')
    print('     --folder-regex [regex] : Use only folders that match the regex')
    print('     --prefix [prefix] : Set a prefix for your file name. Use --preserve-original-filname to use both')
    print('     --preserve-original-filename : Put the original file name in the newly formatted file name')
    print('     --topdown : Walk the directory from the top down')
    print('     --full-match : Fully match file regex(s) instead of searching for them')
    print('')

parser = argparse.ArgumentParser()
parser.add_argument('item')
parser.add_argument('-i', '--info', action='store_true', dest='info')
parser.add_argument('-w', '--walk', action='store_true', dest='walk')
parser.add_argument('-j', '--json', action='store', dest='json')
parser.add_argument('--dry-run', action='store_true', dest='dry_run')
parser.add_argument('--file-regex', action='store', dest='file_regex', nargs='*')
parser.add_argument('--folder-regex', action='store', dest='folder_regex', nargs='*')
parser.add_argument('--prefix', action='store', dest='prefix')
parser.add_argument('--preserve-original-filename', action='store_true', dest='pof')
parser.add_argument('--top-down', action='store_true', dest='topdown')
parser.add_argument('--full-match', action='store_true', dest='full_match')
parser.add_argument('--test', action='store_true', dest='test')

options = WalkOptions(verbose=True)
if __name__ == "__main__":
    if sys.argv[1] == '-h' or sys.argv[1] =='--help':
        usage()
    else:
        args = parser.parse_args()

        if args.dry_run:
            options.set_dry_run(True)

        if args.file_regex:
            options.set_file_regex(args.file_regex)

        if args.folder_regex:
            options.set_folder_regex(args.folder_regex)

        if args.prefix:
            options.set_prefix(args.prefix)

        if args.pof:
            options.set_pof(True)

        if args.topdown:
            options.set_topdown(True)

        if args.full_match:
            options.set_full_match(True)

        if args.json:
            options.set_json(args.json)
            options.parse_json_options()

        if args.test:
            print('[subdivision3]: Test Code')

        if args.walk:
            options.print_options()
            w = Walk(directory=args.item, options=options)
            w.walk()

        if args.info:
            if os.path.isfile(args.item):
                f = File(args.item)
                f.print_info()
            else:
                print('[subdivison3]: Only files supported for now')
