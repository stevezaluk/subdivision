#!/usr/bin/env python3
import os, sys
import re, time
import hashlib, zipfile
from os.path import getsize
from argparse import ArgumentParser
import argparse
from colorama import Fore, Style
from pymediainfo import MediaInfo

def paths():
    print('>> Media Paths')
    print('Main Media: /var/services/homes/szaluk/Drive/media')
    print('Movies: /var/services/homes/szaluk/Drive/media/movies')
    print('TV Shows: /var/services/homes/szaluk/Drive/media/tv-shows')
    print('Anime: /var/services/homes/szaluk/Drive/media/anime')
    print('\n>> Software')
    print('VPKG: /var/services/homes/szaluk/Drive/software')
    print('\n>> Core: ')
    print('Users: /var/services/homes')
    print('Modules: /var/packages')
    print('Binaries: /bin, /usr/bin, /usr/sbin, /usr/local/bin')
    print('SSH Keys: /etc/ssh')
    print('SSL Certificates: /etc/ssl/certs')

def usage():
    print('')
    print(' subdivision - Version 0.2')
    print('')
    print(' usage: ./subdivision [arguments] ITEM')
    print('')
    print('     -h : Show this page')
    print('     -i : Get info on an item')
    # print('         --problems-report : Try to detect formatting problems with the file/dir ')
    print('     -I : Get info on your local drive')
    print(' ')
    print(' Formatting and Directories: ')
    print(' ')
    print('     -w : Do a directory walk')
    print('     -c INT : Create a set ammount of seasons')
    print('     -f : Format an item to be Plex appropriate')
    print('     -d : Remove all .DS_Store files and give all media files r/w/e')
    print('')
    print(' Database Stuff: ')
    print('')
    print('     -a : Add a new series or movie to the database')
    print('     -ma : Mass-Add. Use regexs and add all found shows/movies to the database')
    print('')
    print(' Walk Modifiers: ')
    print('')
    print('     --verbose : Enable more verbosity')
    print('     --dry-run : Do everything except formating')
    print('     --topdown [t/f] : Walk the directory from the top down.')
    print('     --extensions [ext] : Return only specific extensions.')
    print('     --full-match [t/f] : Fully match a regex instead of searching for it')
    print('     --permission [CODE] : Set a different permission bit instead of r/w/e')
    print('     --preserve-original-filename : Preserve the original title in the filename')
    print('     --prefix [PREFIX] : Set a filename prefix: S#E#, YT#, S##E##, s##e##, ROOT#')
    print('     --embed-title : Embed file name into the metadata of the file')
    print('     --file-regex [REGEX] : Only return file names that match the regex')
    print('     --folder-regex [REGEX] : Only return folder names that match the regex')
    # print('     --resolution WxH : Only return media files with specified resolution. Warning: Could take a min')
    # print('     --encoder ENC : Only return media files with specified encoder. Warning: Could take a min')

class Walk(object):
    def __init__(self):
        self.verbose = False
        self.dry_run = False
        self.embed_title = False
        self.preserve_original_filename = False
        self.full_match = False
        self.permission_bit = 0o40777
        self.topdown = True
        self.prefix = False
        self.file_regex = False
        self.folder_regex = False

    def set_var(var, val):
        var = val

    def get_var(var):
        return var

    def directory_walk(self, path, mode=None):
        episode_count = 0
        for root, directories, files in os.walk(self.item, topdown=self.topdown):
            for name in sorted(directories):
                full_path = os.path.join(root, name)
                if mode == 'f' or mode == 'i':
                    match = re.match(r'season(\d+)', name)
                elif mode is None:
                    match = re.match(self.folder_regex, name)

                if match:
                    full_path = os.path.join(root, name)
                    if mode == 'f':
                        season_number = match.group(1)

                    for entry in sorted(os.listdir(full_path)):
                        if mode == 'f' or mode == 'i'
                            episode_regx = [r'(S[0-9])(E[0-9])', r'(S[0-9])\S(E[0-9])\S', r'(s[0-9])(e[0-9])', r'(s\d[0-9])(e\d[0-9])']
                            if entry == '.DS_Store':
                                os.remove('{fp}/.DS_Store')
                            for r in episode_regx:
                                match = re.search(regx, entry)
                                if match:
                                    if mode == 'i':
                                        full_path = os.path.join(root, name)
                                        print(' |--', entry, ' [{g}{s}{nc}]  ({m}{p}{nc})'.format(g=Fore.GREEN, nc=Style.RESET_ALL, m=Fore.MAGENTA, s=os.path.getsize(full_path), p=oct(os.stat(full_path).st_mode)))
                                    file_extension = None
                                    episode_counter = episode_counter + 1
                                    for container in media_containers:
                                        if entry.endswith(container):
                                            file_extension = container
                                            break
                                    full_path = os.path.join(root, name)
                                    old_file_name = '{fp}/{e}'.format(fp=full_path, e=entry)
                                    new_file_name = '{fp}/S{sn}E{en}{ext}'.format(fp=full_path, sn=season_number, en=episode_counter, ext=file_extension)
                                    if self.dry_run:
                                        pass
                                    elif self.dry_run is False:
                                        os.rename(old_file_name, new_file_name)
                                        os.chmod(new_file_name, self.permission_bit)

class Item(Walk):
    def __init__(self, item):
        self.item = item
        self.is_directory = False
        self.prelims()

    def set_item(self, i):
        self.item = i

    def get_item(self):
        return item

    def set_directory(self, dir):
        self.is_directory = dir

    def get_directory(self):
        return self.is_directory

    def prelims(self):
        if os.path.exists(self.item):
            pass
        else:
            print('Error: Item does not exist')
            sys.exit(1)

        if os.path.isdir(self.item):
            self.set_directory(True)
        else:
            self.set_directory(False)

    def issue_report(self):
        pass

    def info(self):
        directory_count = 0
        season_regx = re.compile(r'season(\d+)')
        episode_regx = [r'(S[0-9])(E[0-9])', r'(S[0-9])\S(E[0-9])\S', r'(s[0-9])(e[0-9])', r'(s\d[0-9])(e\d[0-9])']
        print('Item: ', self.item)
        print('Size:', getsize(self.item))
        print('Permissions: ', oct(os.stat(self.item).st_mode))
        print('Last Modified: ', time.ctime(os.stat(self.item).st_mtime))
        print('File Owner UID: ', os.stat(self.item).st_uid)
        print('File Owner GID: ', os.stat(self.item).st_gid)

        if self.is_directory:
            if self.item.isupper():
                print('\n>> Episode Map: ') # TODO:

            for root, directories, files in os.walk(self.item, topdown=True):
                for name in sorted(directories):
                    directory_count = directory_count + 1
                    full_path = os.path.join(root, name)
                    match = season_regx.match(name)
                    if match:
                        print(' |-[{m}{x}{nc}]'.format(x=root, m=Fore.RED, nc=Style.RESET_ALL), name)
                        for entry in sorted(os.listdir(full_path)):
                            for regx in episode_regx:
                                match = re.search(regx, entry)
                                if match:
                                    full_path = os.path.join(root, name)
                                    print(' |--', entry, ' [{g}{s}{nc}]  ({m}{p}{nc})'.format(g=Fore.GREEN, nc=Style.RESET_ALL, m=Fore.MAGENTA, s=os.path.getsize(full_path), p=oct(os.stat(full_path).st_mode)))
        else:
            media_file_exts = ['.mkv', '.mp4', '.m4v']
            archive_file_exts = ['.zip', '.rar', '.tar.gz']
            file_name, file_ext = os.path.splitext(self.item)
            audio_track_count = 0
            for ext in media_file_exts:
                if ext == file_ext:
                    media_info = MediaInfo.parse(self.item)
                    for track in media_info.tracks:
                        if track.track_type == 'General':
                            print('\n>> General')
                            print(' Title: ', track.title)
                            print(' Author: ', track.author)
                            print(' Description: ', track.description)
                            print('\n Duration: ', track.other_duration[1])
                            print(' Date Encoded: ', track.encoded_date)
                            print(' Writing Application: ', track.writing_application)
                            print(' Writing Library: ', track.writing_library)
                            print(' Overall Bit Rate: ')
                        elif track.track_type == 'Video':
                            print('\n>> Video')
                            print(' Encoding Lib: ', track.encoded_library_name)
                            print(' Resolution: {w}x{h}'.format(w=track.width, h=track.height))
                            print(' Aspect Ratio: ', track.other_display_aspect_ratio[0])
                            print(' Frame Rate: ', track.frame_rate)
                            print(' Bit Rate: ', track.bit_rate)
                            print(' Bit Depth: ', track.bit_depth)
                        elif track.track_type == 'Audio':
                            audio_track_count = audio_track_count + 1
                            print('\n>> Audio #{}'.format(audio_track_count))
                            print(' Language: ', track.language)
                            print(' Codec: ', track.codec)
                            print(' Bit Rate: ', track.bit_rate)
                    break
                    sys.exit(0)

            if file_ext == '.zip':
                contents = []
                with zipfile.ZipFile(self.item, 'r') as zipobj:
                    objects = zipobj.infolist()
                    for object in objects:
                        zip_comment = object.comment
                        contents.append(object.filename)

                    print('\n>> Zip File')
                    print(' Comment: ', zip_comment)
                    print(' Compressed Size: ', getsize(self.item))
                    print('\n>> Contents')
                    for c in contents:
                        print(' -', c)

    def format(self):
        if self.is_directory is False:
            print('Directory is False. Formatting support for single files coming')
            sys.exit(0)

        if self.dry_run is False:
            yn = input('[WARNING] Dry Run is set to False. All downloaded media files will be formated. Are you sure you want to proceed: ')
            if yn == 'yes' or yn == 'Yes' or yn == 'y' or yn == 'Y':
                pass
            else:
                sys.exit(1)
        season_regx = r'season(\d+)'
        episode_regx = [r'(S[0-9])(E[0-9])', r'(S[0-9])\S(E[0-9])\S', r'(s[0-9])(e[0-9])', r'(s\d[0-9])(e\d[0-9])']
        media_containers = ['.mkv', '.mp4', '.m4v'] # write support for limited containers

        print('Item: ', self.item)
        episode_counter = 0
        for root, directories, files in os.walk(self.item, topdown=True):
            for name in sorted(directories):
                full_path = os.path.join(root, name)
                match = re.match(season_regx, name)
                if match:
                    full_path = os.path.join(root, name)
                    season_number = match.group(1)
                    for entry in sorted(os.listdir(full_path)):
                        if entry == '.DS_Store':
                            print('{r}Removed File{nc}: .DS_Store'.format(r=Fore.RED, nc=Style.RESET_ALL))

                        for regx in episode_regx:
                            match = re.search(regx, entry)
                            if match:
                                for container in media_containers:
                                    if entry.endswith(container):
                                        file_extension = container
                                        break
                                episode_counter = episode_counter + 1
                                full_path = os.path.join(root, name)
                                print('{g}Formated File{nc}: {fp}/{e} -> S{sn}E{en}{ext}'.format(fp=full_path, e=entry, np=new_path, g=Fore.GREEN, nc=Style.RESET_ALL, sn=season_number, en=episode_number, ext=file_extension))
                                old_file_name = '{fp}/{e}'.format(fp=full_path, e=entry)
                                new_file_name = '{fp}/S{sn}E{en}{ext}'.format(fp=full_path, sn=season_number, en=episode_counter, ext=file_extension)

                episode_counter = 0

parser = ArgumentParser()
parser.add_argument('item')
parser.add_argument('-i', '--info', action='store_true', dest='info')
parser.add_argument('-f', '--format', action='store_true', dest='format')
parser.add_argument('-t', '--test', action='store_true', dest='test')

parser.add_argument('--dry-run', action='store_true', dest='dry_run')
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Error: Missing item path')
        usage()

    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        usage()
    else:
        args = parser.parse_args()
        item = Item(args.item)

        if args.test:
            print('Test Function')
            rgx = r'season(\d+)'
            string = 'season3'
            match = re.search(rgx, string)
            print(match.group(1))

        if args.dry_run:
            item.set_dry_run(True)

        # if args.verbose:
        #     item.set_verbosity(True)

        if args.info:
            item.info()

        if args.format:
            item.format()
