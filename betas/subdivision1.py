#!/usr/bin/env python3
import sys, os, subprocess, argparse
import re, hashlib, zipfile
import time
from os.path import getsize
import stat
try:
    import imdb, psutil
    from pymediainfo import MediaInfo
    from colorama import Style, Fore, Back
    import psycopg2
    from pymongo import MongoClient
except ModuleNotFoundError:
    print('[!] Missing dependencies')
    print('[!] Required Dependencies: IMDbPy, psutil, pymediainfo, zipfile, rarfile, colorama')

#from teletype.components import SelectOne, ChoiceHelper

# sudo docker run -d -p 27017:27017 -v ~/data:/data/db mongo   || create mongodb docker instance
# docker exec -it [contianer_name] bash || Shell into container
# docker exec -it [container_name] mongo || Mongo shell into contianer
# docker kill [contianer_name] || kill container
# docker rm [container_name] || Remove container completely
# docker inspect [container_name] || Find usefull info about container

def yes_or_no(text):
    good = False
    while good is False:
        yn = input(text)
        if yn == 'Yes' or yn == 'yes' or yn == 'y' or yn == 'Y':
            good = True
        elif yn == 'No' or yn == 'no' or yn == 'n' or yn == 'N':
            sys.exit(1)
        else:
            print('[!] Answer yes or no')

def replace_tilda(text):
    home = os.getenv("HOME")
    if text.startswith('~'):
        new_text = text.replace('~', home)
        return new_text
    else:
        return text

def test():
    # client = MongoClient('localhost', 27017)

    # database = client['vaultdb']
    # results = database['vpkg'].find({"name": "package1"})
    # for result in results:
    #     print(result)

    # iii = oct(os.stat("/Users/szaluk/Desktop/accounts.txt")[ST_MODE])
    # print(os.stat('/Users/szaluk/Desktop/'))

    path = '~/Desktop'
    new_path = replace_tilda(path)
    print(path)
    print(new_path)

def usage():
    print('')
    print(' {m}subdivision{nc} - version 0.1'.format(m=Fore.MAGENTA, nc=Style.RESET_ALL))
    print(' Built with python3, pymediainfo, and IMDbPy')
    print('')
    print(' usage: subdivision [arguments] {file/directory}')
    print('')
    print(' Basic Operations: ')
    print(' ')
    print('     -h : Print this screen of text')
    print('     -i : Print all information for a directory, a file, or a piece of media')
    print('     -I : Print local information about your hard drive, fs, and connected storage devices')
    print('     -gnfo : Generate an .nfo file for a file')
    print('')
    print(' Media Files: ')
    print(' ')
    print('     -w [tag] [content] : Write metadata to a media file')
    print('     --hash : Print all the checksums of a file')
    print('     --verify [hash] : Verify a checksum with a files hash')
    print('')
    print(' IMDB: ')
    print(' ')
    print('     -s : Interactively search IMDB for a piece of media')
    print('     -e [media_id] : Print an episode map for a piece of media based on media id')
    print('')
    print(' Formating & Directories: ')
    print(' ')
    print('     -C [int] [directory] : Add a specific number of seasons to a directory with r/w/e permissions')
    print('     -r : Rebuild VAULTs directory structure on the local backup disk')
    print('     -F : Format a single episode or an entire series.')
    print('         --limit-season [int] : Limit the ammount of seasons to format')
    print('         --dry-run : Wont rename the files. Just shows you what need to be done')
    print('     -ds, --remove-ds-store : Remove all .DS_Store files recursivelly in a directory')
    print('')
    print(' Compression, Archiving, & Encryption: ')
    print(' ')
    print('     -c [file_type] : Compress a directory into a zip, rar, or tar.gz archive')
    print('     -e [bit_size] [key] : Encrypt a file in AES with a specified bit size')
    print('')
    print(' Debug: ')
    print(' ')
    print('     --test : Test argument')
    print('     --info-sets [file] : Print infosets for pymediainfo')
    print('     --imdb-sets [file] : Print infosets for IMDbPy')
    print('     --useful-paths : Print useful paths to know for VAULT\n')

def usefull_paths():
    print('>>> Media Related Paths: ')
    print('Media Directory: /var/services/homes/szaluk/Drive/media')
    print('Movies Directory: /var/services/homes/szaluk/Drive/media/movies')
    print('TV Show Directory: /var/services/homes/szaluk/Drive/media/tv-shows')
    print('Anime Directory: /var/services/homes/szaluk/Drive/media/anime')
    print('Anime Movies Directory: /var/services/homes/szaluk/Drive/media/anime/anime-movies')
    print('VPKG Directory: /var/services/homes/szaluk/Drive/packages')

    print('\n>>> Core Directories: ')
    print('Users: /var/services/homes')
    print('Installed Modules: /var/packages')
    print('Binaries: /bin, /usr/bin, /usr/sbin, /usr/local/bin')
    print('SSH Keys: /etc/ssh')
    print('SSL Certificates: /etc/ssl/certs')
    print('Core Volume Directory: /volume1')

def get_disk_info():
    partitions = psutil.disk_partitions()
    io_counters = psutil.disk_io_counters()

    print('>>> Local Disk')
    print('[*] IO Counters: ')
    print('Read Count: ', io_counters.read_count)
    print('Write Count: ', io_counters.write_count)
    print('Read Bytes: ', io_counters.read_bytes)
    print('Write Bytes: ', io_counters.write_bytes)
    print('Read Time: ', io_counters.read_time)
    print('Write Time: ', io_counters.write_time)
    print()
    root_du = psutil.disk_usage('/')
    print('[*] Disk Usage: /')
    print('Total: ', root_du.total)
    print('Used: ', root_du.used)
    print('Free: ', root_du.free)
    print('Percent: ', root_du.percent, '% \n')
    print('[*] Partitions:')
    for partition in partitions:
        print('Device: ', partition.device)
        print('Mount Point: ', partition.mountpoint)
        print('Filesystem Type: ', partition.fstype)
        print('Options: ', partition.opts, '\n')
    volume_backup_path = ' /Volumes/VAULTBACKUP'
    if os.path.exists(volume_backup_path):
        vb_du = psutil.disk_usage(volume_backup_path)
        print('\n>>> Backup Disk')
        print('[*] Disk Usage: ', volume_backup_path)
        print('Total: ', vb_du.total)
        print('Used: ', vb_du.used)
        print('Free: ', vb_du.free)
        print('Percent: ', vb_du.percent)

class File(object):
    def __init__(self, path, verbose=False):
        super(File, self).__init__()
        self.path = path
        self.verbose = verbose
        self.check_file_existance(path)
        self.season_regex = r'season\S+'
        self.episode_regex_1 = r'(S[0-9])(E[0-9])'
        self.episode_regex_2 = r'(S[0-9])\S(E[0-9])\S'
        self.episode_regex_3 = r'(s[0-9])(e[0-9])'
        self.episode_regex_4 = r'(s\d[0-9])(e\d[0-9])'

    def get_path(self):
        return self.path

    def set_path(self, new_path):
        self.path = new_path

    @classmethod
    def check_file_existance(self, path):
        if os.path.exists(path):
            pass
        else:
            print('[!] File not found')
            sys.exit(0)

    def get_info(self):
        video_track_count = 0
        audio_track_count = 0
        subtitle_track_count = 0
        total_track_count = 0

        has_title_tag = False

        if self.path.endswith('.mp4') or self.path.endswith('.mkv') or self.path.endswith('.m4v') or self.path.endswith('.webm'):
            media_info = MediaInfo.parse(self.path)
            for track in media_info.tracks:
                if track.track_type == 'General':
                    print('>>> General Information')
                    print('File: ', self.path)
                    print('Title: ', track.title)
                    if track.title is None:
                        has_title_tag = False
                    else:
                        has_title_tag = True
                        title = track.title
                    print('File Size: ', track.other_file_size[0])
                    print('Date Encoded: ', track.encoded_date)
                    print('Unique ID: ', track.unique_id)
                    print('Duration: ', track.other_duration[1])
                    print('Container: ', track.container)
                    print('Format: ', track.format)
                    print()
                elif track.track_type == 'Video':
                    total_track_count = total_track_count + 1
                    video_track_count = video_track_count + 1
                    print('>>> Video Track')
                    print('Resolution: {w}x{h}'.format(w=track.width, h=track.height))
                    print('Encoder: ', track.encoded_library_name)
                    print('Pixel Aspect Ratio: ', track.pixel_aspect_ratio)
                    print('Bit Rate: ', track.bit_rate)
                    print('Bit Depth: ', track.bit_depth)
                    print('Frame Rate: ', track.frame_rate)
                    if self.verbose:
                        print('Encoded Settings: ', track.encoding_settings)
                    print()
                elif track.track_type == 'Audio':
                    total_track_count = total_track_count + 1
                    audio_track_count = audio_track_count + 1
                    print('>>> Audio Track')
                    print('Codec: ', track.codec_id)
                    print('Bit Rate: ', track.bit_rate)
                    print('Languages: ', track.language)
                    print('Channels: ', track.channel)
                    print()
                elif track.track_type == 'Text':
                    total_track_count = total_track_count + 1
                    subtitle_track_count = subtitle_track_count + 1
                    print('>>> Subtitle Track')
                    print('Language: ', track.language)
                    print('Hard Coded: ', track.forced)
                    print()

            print('>>> Post Information: ')
            print('Total Counted Tracks: ', total_track_count)
            print('Video Tracks: ', video_track_count)
            print('Audio Tracks: ', audio_track_count)
            print('Subtitle Tracks: ', subtitle_track_count, '\n')

            print('>>> Formatting Information')
            match1 = re.search(self.episode_regex_1, self.path)
            match2 = re.search(self.episode_regex_2, self.path)
            match3 = re.search(self.episode_regex_3, self.path)
            match4 = re.search(self.episode_regex_4, self.path)

            if match1 is None and match2 is None and match3 is None and match4 is None:
                print('[!] Failed to find season/episode prefix')
            elif match1:
                print('Season/Episode Prefix: ', match1.group(0))
            elif match2:
                print('Season/Episode Prefix: ', match2.group(0))
            elif match3:
                print('Season/Episode Prefix: ', match3.group(0))
            elif match4:
                print('Season/Episode Prefix: ', match4.group(0))

            if has_title_tag:
                print('Title Tag Found: ', title)
            elif has_title_tag is False:
                print('[!] Failed to find title tag')

            permission_bit = os.stat(self.path).st_mode
            print('Permission Bit: ', permission_bit)

        elif self.path.endswith('.zip'):
            contents = []
            content_size = 0
            with zipfile.ZipFile(self.path, 'r') as zipobj:
                objects = zipobj.infolist()
                for object in objects:
                    content_size = content_size + object.file_size/1000000
                    string = ' * {fn}     {fs} MiB'.format(fn=object.filename, fs=object.file_size/1000000)
                    comment = object.comment
                    contents.append(string)
            stats = os.stat(self.path)

            print('>>> General Information')
            print('File: ', self.path)
            print('Creation Date: ', time.ctime(stats.st_ctime))
            print('Comment: ', comment)
            print('File Type: ZIP Archive File Format\n')
            print('>>> Contents: ')
            for member in contents:
                print(member)
            print('Content Size: ', content_size, 'MiB')
        elif self.path.endswith('.rar'):
            print('[!] RAR File not supported yet')
        elif self.path.endswith('.tar') or self.path.endswith('.tar.gz'):
            print('[!] TAR/TARGZ File not supported yet')
        else:
            print('[!] File Not Supported')

        if self.verbose:
            hashes = self.get_hashes()
            print('>>> Hashes')
            print('MD5: ', hashes[3])
            print('SHA-1: ', hashes[0])
            print('SHA-256: ', hashes[1])
            print('SHA-512: ', hashes[2])

    def get_hashes(self):
        ret = []

        with open(self.path, mode='rb') as file:
            data = file.read()
            sha1 = hashlib.sha1(data).hexdigest()
            sha256 = hashlib.sha256(data).hexdigest()
            sha512 = hashlib.sha512(data).hexdigest()
            md5 = hashlib.md5(data).hexdigest()
        file.close()

        ret.insert(0, sha1)
        ret.insert(1, sha256)
        ret.insert(2, sha512)
        ret.insert(3, md5)

        return ret

    def format(self): # integrate this with info and do the same for directories
        container_list = ['.mp4', '.m4v', '.mkv', '.webm']
        valid_container = False

        print('>>> Scanning File: ', self.path)
        # check for season/episode prefix
        match1 = re.search(self.episode_regex_1, self.path)
        match2 = re.search(self.episode_regex_2, self.path)
        match3 = re.search(self.episode_regex_3, self.path)
        match4 = re.search(self.episode_regex_4, self.path)

        if match1 is None and match2 is None and match3 is None and match4 is None:
            print('[!] Failed to find season/episode prefix')
        elif match1:
            print('[+] Found season/episode prefix: ', match1.group(0))
        elif match2:
            print('[+] Found season/episode prefix: ', match2.group(0))
        elif match3:
            print('[+] Found season/episode prefix: ', match3.group(0))
        elif match4:
            print('[+] Found season/episode prefix: ', match4.group(0))

        for container in container_list:
            if self.path.endswith(container):
                valid_container = True
                print('[+] Valid Media Container Detected: ', container)

        if valid_container is False:
            print('[!] No Valid Media Container found: Container should be mp4, mkv, m4v, or webm')

        media_info = MediaInfo.parse(self.path)
        for track in media_info.tracks:
            if track.track_type == 'General':
                if track.title is None:
                    print('[!] No "title" tag content. ')
                    break
                elif track.title:
                    print('[+] Found "title" tag: ', track.title)
                    break
        print()


class Directory(object):
    def __init__(self, path):
        super(Directory, self).__init__()
        self.path = path
        self.check_file_existance(path)
        self.season_regex = r'season\d+'
        self.grouped_season_regex = r'season(\d+)'
        self.episode_regex_1 = r'(S[0-9])(E[0-9])'
        self.episode_regex_2 = r'(S[0-9])\S(E[0-9])\S'
        self.episode_regex_3 = r'(s[0-9])(e[0-9])'
        self.episode_regex_4 = r'(s\d[0-9])(e\d[0-9])'

    def set_path(self, new_path):
        self.path = new_path

    def get_path(self):
        return self.path

    @classmethod
    def check_file_existance(self, path):
        home = os.getenv("HOME")
        if os.path.exists(path):
            pass
        else:
            print('[!] Directory not found')
            sys.exit(1)

    def get_info(self):
        total_file_count = 0
        media_file_count = 0
        season_count = 0
        episode_count = 0

        directory_list = []
        season_list = []
        episode_list = []
        print('>>> General Information')
        print('Directory: ', self.path, '\n')

        for entry in os.scandir(self.path):
            member = entry.path
            if os.path.isdir(member):
                directory_list.append(member)

            total_file_count = total_file_count + 1

            if member.endswith('.mkv') or member.endswith('.mp4') or member.endswith('.m4v') or member.endswith('.webm'):
                total_file_count = total_file_count + 1
                media_file_count = media_file_count + 1

        for entry in os.listdir(self.path):
            season_match = re.search(self.season_regex, entry)
            if season_match is None:
                pass
            elif season_match:
                season_count = season_count + 1
                season_list.append(entry)

            episode_match1 = re.search(self.episode_regex_1, entry)
            episode_match2 = re.search(self.episode_regex_2, entry)
            episode_match3 = re.search(self.episode_regex_3, entry)
            episode_match4 = re.search(self.episode_regex_4, entry)

            if episode_match1 is None and episode_match2 is None and episode_match3 is None:
                pass
            elif episode_match1:
                episode_count = episode_count + 1
                episode_list.append(entry)
            elif episode_match2:
                episode_count = episode_count + 1
                episode_list.append(entry)
            elif episode_match3:
                episode_count = episode_count + 1
                episode_list.append(entry)
            elif episode_match4:
                episode_count = episode_count + 1
                episode_list.append(entry)

        for directory in directory_list:
            for entry in os.listdir(directory):
                total_file_count = total_file_count + 1
                season_match = re.search(self.season_regex, entry)
                if season_match is None:
                    pass
                elif season_match:
                    season_count = season_count + 1
                    # total_file_count = total_file_count + 1
                    season_list.append(entry)

                episode_match1 = re.search(self.episode_regex_1, entry)
                episode_match2 = re.search(self.episode_regex_2, entry)
                episode_match3 = re.search(self.episode_regex_3, entry)
                episode_match4 = re.search(self.episode_regex_4, entry)

                if episode_match1 is None and episode_match2 is None and episode_match3 is None and episode_match4 is None:
                    pass
                elif episode_match1:
                    # total_file_count = total_file_count + 1
                    episode_count = episode_count + 1
                    episode_list.append(entry)
                elif episode_match2:
                    # total_file_count = total_file_count + 1
                    episode_count = episode_count + 1
                    episode_list.append(entry)
                elif episode_match3:
                    # total_file_count = total_file_count + 1
                    episode_count = episode_count + 1
                    episode_list.append(entry)
                elif episode_match4:
                    episode_count = episode_count + 1
                    episode_list.append(entry)

        print('>>> Seasons: ')
        for season in season_list:
            print('-', season)

        print('\n>>> Episodes: ')
        for episode in episode_list:
            print('-', episode)

        print('\n>>> Post Information: ')
        print('Total Items: ', total_file_count - 1)
        print('Total Directory Size: \n')
        print('Seasons Count: ', season_count)
        print('Episodes Count: ', episode_count)
        print('Total Media Files: ', media_file_count)

    def create_seasons(self, number):
        yn = input('Are you sure you want to add {} seasons? [y/n]: '.format(number))
        if yn == 'yes' or yn == 'y' or yn == 'Y':
            for i in range(1, int(number) + 1):
                if self.path.endswith('/'):
                    directory = '{pd}season{int}'.format(pd=self.path, int=i)
                    os.mkdir(directory, 0o777)
                else:
                    pd1 = '{}/'.format(self.path)
                    directory = '{pd}season{int}'.format(pd=pd1, int=i)
                    os.mkdir(directory, 0o777)
        elif yn == 'no' or yn == 'n' or yn == 'N' or yn == 'No':
            sys.exit(0)
        else:
            print('Invalid response')
            sys.exit(0)

    def format(self, dry_run=False, limit_seasons=None):
        total_file_count = 0
        file_count = 0
        directory_count = 0

        container_list = ['.mp4', '.mkv', '.m4v', '.webm']

        print('>>> Directory: ', self.path)
        for root, directories, files in os.walk(self.path, topdown=True):
            for name in sorted(directories):
                directory_count = directory_count + 1
                season_match = re.search(self.season_regex, name)
                if season_match is None:
                    print('[-] Skipping directory with invalid season naming: ', name)
                    directories.remove(name) # possible error: I dont thiknk it is actually removing dir's herre

            for name in sorted(files):
                if name == '.DS_Store':
                    full_path = os.path.join(root, name)
                    print('Removing: .DS_Store file')
                    os.remove(full_path)
                else:
                    total_file_count = total_file_count + 1
                    for container in container_list:
                        if name.endswith(container):
                            valid_container = True
                            file_ext = container

                    full_path = os.path.join(root, name)

                    if valid_container is False:
                        print('[-] Skipping file with invalid extension: ', name)
                        files.remove(name) # error here: file still passes this and the program will try to rename it

                    file_count = file_count + 1
                    valid_container = False

                    season_number = re.search(self.grouped_season_regex, root).group(1)
                    new_name = 'S{sn}E{en}{ext}'.format(sn=season_number, en=file_count, ext=file_ext)
                    new_path = os.path.join(root, new_name)
                    print('Renaming File: ', full_path, '  ->  ', new_path)
                    if dry_run is False:
                        os.rename(full_path, new_path)
                        os.chmod(full_path, 0o100777)
            file_count = 0

            print('\n[+] Renamed {} files'.format(total_file_count))

    def remove_ds_store(self):
        removed_file_count = 0

        print('>>> Directory: ', self.path)
        for root, directories, files in os.walk(self.path, topdown=True):
            for name in files:
                if name == '.DS_Store':
                    removed_file_count = removed_file_count + 1
                    print('Removing: .DS_Store file')
                    full_path = os.path.join(root, name)
                    os.remove(full_path)

        print('[+] Removed {} files'.format(removed_file_count))

    def compress(self, archive=None):
        if archive is None:
            pass
        elif archive == 'zip':
            pass

# parser = argparse.ArgumentParser()
#
# parser.add_argument('-I',  dest='local_disk_info', action='store_true', help="Print information about your local disks")
# parser.add_argument('-i', dest='info', action='store', help="Print information about a file, directory, or archvie")
# parser.add_argument('-t', '--test', dest='_test', action='store_true', help="Test Function")

if __name__ == '__main__':
    if sys.argv[1] == '-h':
        usage()
    elif sys.argv[1] == '-i':
        if sys.argv[2].startswith('~'):
            item = sys.argv[2].replace('~', '/Users/szaluk/')
        else:
            item = sys.argv[2]
        if item.endswith('.mp4') or item.endswith('.mkv') or item.endswith('.m4v') or item.endswith('.zip') or item.endswith('.rar'):
            f = File(item)
            f.get_info()
        else:
            d = Directory(item)
            d.get_info()
    elif sys.argv[1] == '-I':
        get_disk_info()
    elif sys.argv[1] == '-C':
        if sys.argv[3].startswith('~'):
            item = sys.argv[3].replace('~', '/Users/szaluk')
        else:
            item = sys.argv[3]

        if item.endswith('.mp4') or item.endswith('.mkv') or item.endswith('.m4v') or item.endswith('.zip') or item.endswith('.rar'):
            print('[!] Cannot create directories inside of a file')
        else:
            d = Directory(item)
            d.create_seasons(sys.argv[2])
    elif sys.argv[1] == '-F':
        print('[-] The format function cannot handle any non media files for now')
        print('[-] Please make sure all non media files are taken out of all of your')
        print('[-] Directories before you use this tool.')
        yes_or_no('[!] Are you sure you want to continue? [y/n]: ')

        if sys.argv[2].startswith('~'):
            item = sys.argv[2].replace('~', '/Users/szaluk')
        else:
            item = sys.argv[2]

        if sys.argv[2].endswith('.mp4') or sys.argv[2].endswith('.mkv') or sys.argv[2].endswith('.m4v') or sys.argv[2].endswith('.webm'):
            f = File(item)
            f.format()
        elif sys.argv[2].endswith('.zip') or sys.argv[2].endswith('.rar') or sys.argv[2].endswith('.tar.gz'):
            print('[!] Will not format scan a compressed archive')
        else:
            d = Directory(item)
            d.format(dry_run=True)
    elif sys.argv[1] == '-c':
        if sys.argv[3].startswith('~'):
            item = sys.argv[3].replace('~', '/Users/szaluk')
        else:
            item = sys.argv[3]

        archive_type = sys.argv[2]

        d = Directory(item)
        if archive_type == 'zip':
            d.compress(archive='zip')
    elif sys.argv[1] == '-ds' or '--remove-ds-store':
        # if sys.argv[2].startswith('~'):
        #     item = sys.argv[2].replace('~', '/Users/szaluk')
        # else:
        #     item = sys.argv[2]

        # d = Directory(item)
        # d.remove_ds_store()
        pass
    elif sys.argv[1] == '--test':
        test()
    elif sys.argv[1] == '--hash':
        if sys.argv[2].startswith('~'):
            item = sys.argv[2].replace('~', '/Users/szaluk/')
        else:
            item = sys.argv[2]
        if item.endswith('.mp4') or item.endswith('.mkv') or item.endswith('.m4v') or item.endswith('.zip') or item.endswith('.rar'):
            f = File(item)
            hashes = f.get_hashes()
            print('>>> Hashes')
            print('MD5: ', hashes[3])
            print('SHA-1: ', hashes[0])
            print('SHA-256: ', hashes[1])
            print('SHA-512: ', hashes[2])
    elif sys.argv[1] == '--verify':
        pass
    elif sys.argv[1] == '--usefull-paths':
        usefull_paths()
    else:
        print('[!] Invalid Argument')

    # args = parser.parse_args()
    #
    # if args.local_disk_info:
    #     get_disk_info()
    #
    # if args.info:
    #     if os.path.isdir(args.info):
    #         item = replace_tilda(args.info)
    #         d = Directory(item)
    #         d.get_info()
    #     elif os.path.isfile(args.info):
    #         item = replace_tilda(args.info)
    #         f = File(item)
    #         f.get_info()
    #     else:
    #         print('[!] Invalid argument')
    #
    # if args._test:
    #     test()
