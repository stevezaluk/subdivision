import os, sys, time, pwd, grp, re

home = os.getenv("HOME")

"""
    WalkOptions - A template for the settings
        verbose (bool) - Enable Printing
        topdown (bool) - Walk the directory from the top down
        use_regex (bool) - A bool to determine wether or not to spend time matching file names to a regex
        file_regex (str, list) - The file regex to match against
        folder_regex (str, list) - The directory regex to match against
        use_format (bool) - A bool to determine wether or not to spend time formating files
        prefix (str) - Rename each file to start with this. If preserve_original_filename is not turned on. It will rename the file to the prefix
        embed_title - Embed the newly formatted file name into a media files "title" metadata field
        preserve_original_filename - Add the original filename to the end of the newly formated file name

    Prefixs':
        self.prefix can either be a regular string or it can be season+episode. Setting the prefix field to
        season+episode will search for a S#E# variant and rename the file to that tag if found. This makes it
        easy to quickly format files for plex/emby. I would love to add the title of the episode to the end
        of the file name to but that would be a bitch to automate.

    Regexs':
        self.folder_regex or self.file_regex can either be a list of regex's or a string. If a list is used
        then it will iterate through the list and if a item name matches ONE of the regular expressions then it
        will pass the direectories/files to the next stage. On a side note, self.file_regex uses r.search()
        instead of r.match(). This makes it easy to search for S#E# tags. I plan to add options in the future
        to one, add the ability to do a full match on self.file_regex and to match all the regex's in a list
        instead of just one.
"""
class WalkOptions(object):
    def __init__(self, verbose=None, topdown=None, extensions=None, use_regex=False,
                    file_regex=None, folder_regex=None, use_format=False,
                    dry_run=None, prefix=None, embed_title=None, preserve_original_filename=None):
        self.verbose = verbose
        self.topdown = topdown
        self.extensions = extensions
        self.use_regex = use_regex
        self.file_regex = file_regex
        self.folder_regex = folder_regex
        self.use_format = use_format
        self.dry_run = dry_run
        self.prefix = prefix
        self.embed_title = embed_title
        self.preserve_original_filename = preserve_original_filename

    ### GETTERS AND SETTERS ###
    def set_verbose(self, v):
        if isinstance(v, bool):
            self.verbose = v
        else:
            print('[sprint][ERROR]: "verbose" must be a boolean')
            sys.exit(0)

    def get_verbose(self):
        return self.verbose

    def set_topdown(self, t):
        if isinstance(t, bool):
            self.topdown = t
        else:
            print('[sprint][ERROR]: "topdown" must be a boolean')
            sys.exit(0)

    def get_topdown(self):
        return self.topdown

    def set_extensions(self, e):
        self.extensions = e

    def get_extensions(self):
        return self.extensions

    def set_regex(self, r):
        if isinstance(r, bool):
            self.use_regex = r
        else:
            print('[sprint][ERROR]: "full_match" must be a boolean')

    def get_regex(self):
        return self.use_regex

    def set_file_regex(self, r):
        self.file_regex = r
        self.set_regex(True)

    def get_file_regex(self):
        return self.file_regex

    def set_folder_regex(self, r):
        self.folder_regex = r
        self.set_regex(True)

    def get_folder_regex(self):
        return self.folder_regex

    def set_rename(self, r):
        if isinstance(r, bool):
            self.use_format = r
        else:
            print('[sprint][ERROR]: "rename" must be a boolean')
            sys.exit(0)

    def get_rename(self):
        return self.use_format

    def set_dry_run(self, d):
        if isinstance(d, bool):
            self.dry_run = d
        else:
            print('[sprint][ERROR]: "dry_run" must be a boolean')
            sys.exit(0)

    def get_dry_run(self):
        return self.dry_run

    def set_prefix(self, p):
        if isinstance(p, str):
            self.prefix = p
            self.use_format = True
        else:
            print('[sprint][ERROR]: "prefix" must be a string')
            sys.exit(0)

    def get_prefix(self):
        return self.prefix

    def set_embed_title(self, e):
        if isinstance(e, str):
            self.embed_title = e
            self.use_format = True
        else:
            print('[sprint][ERROR]: "embed_title" must be a string')
            sys.exit(0)

    def get_embed_title(self):
        return self.embed_title

    def set_pof(self, p):
        if isinstance(p, bool):
            self.preserve_original_filename = p
            self.use_format = True
        else:
            print('[sprint][ERROR]: "preserve_original_filename" must be a boolean')
            sys.exit(0)

    def get_pof(self):
        return self.preserve_original_filename

    def print_options(self):
        print('[*] Walk Options: ')
        print(' Verbose: ', self.get_verbose())
        print(' Top Down: ', self.get_topdown())
        print(' File Regex: ', self.get_file_regex())
        print(' Folder Regex: ', self.get_folder_regex())
        # print(' Perscribed Extensions: ', self.get_extensions())
        print('\n[*] Format Options: ')
        print(' Dry Run: ', self.get_dry_run())
        print(' Prefix: ', self.get_prefix())
        # print(' Embed Title: ', self.get_embed_title())
        print(' Preserve Original Filename: ', self.get_pof())
        print('')

"""
    File - An object representing a file present on the users hard drive

    Everytime this object is called it re-scans the file to fill in, its instance
    variables. This is also done whenever chmod(), rename(), and move() are called.
"""
class File(object):
    def __init__(self, path): # need absolute path instance variable
        self.path = path
        self.absolute_path = None
        self.file_name = None
        self.file_extension = None
        self.file_size = None
        self.modified_date = None
        self.creation_date = None
        self.file_permissions = None
        self.owner = None
        self.group = None
        self.owner_gid = None
        self.owner_uid = None
        self.scan()

    def get_path(self):
        return self.path

    def get_absolute_path(self):
        return self.absoulute_path

    def get_file_name(self):
        return self.file_name

    def get_file_extension(self):
        return self.file_extension

    def get_file_size(self):
        return self.file_size

    def get_modified_date(self):
        return self.modified_date

    def get_creation_date(self):
        return self.modified_date

    def get_file_permissions(self):
        return self.file_permissions

    def get_owner(self):
        return self.owner

    def get_group(self):
        return self.group

    def get_owner_gid(self):
        return self.owner_gid

    def get_owner_uid(self):
        return self.owner_uid

    def move(self, new_location):
        os.mv(self.path, new_location)
        self.scan()

    def remove(self):
        os.remove(self.path)
        self.scan()

    def rename(self, new_name):
        os.rename(self.absolute_path, new_name)
        self.scan()

    def chmod(self, code):
        os.chmod(self.path, code)
        self.scan()

    def check_file_existance(self):
        if self.path.startswith('~'):
            self.path = self.path.replace('~', home)

        if os.path.exists(self.path):
            pass
        else:
            print('[sprint][ERROR]: File does not exist ({})'.format(self.path))

    def scan(self):
        self.check_file_existance()
        if self.path.startswith('~'):
            self.path = self.path.replace('~', home)

        if os.path.isfile(self.path):
            self.absolute_path = os.path.abspath(self.path)
            self.file_name = self.path.split('/')[-1]
            self.file_extension = os.path.splitext(self.absolute_path)[1]
            self.file_size = os.stat(self.path).st_size
            self.modified_date = time.ctime(os.stat(self.path).st_mtime)
            self.creation_date = time.ctime(os.stat(self.path).st_ctime)
            self.file_permissions = oct(os.stat(self.path).st_mode)
            self.owner_uid = os.stat(self.path).st_uid
            self.owner_gid = os.stat(self.path).st_gid
            self.owner = pwd.getpwuid(self.owner_uid).pw_name
            self.group = grp.getgrgid(self.owner_gid).gr_name

    def print_info(self):
        print('Absolute Path: ', self.absolute_path)
        print('File Name: ', self.file_name)
        print('File Extension: ', self.file_extension)
        print('File Size (bytes): ', self.file_size)
        print('Creation Date: ', self.creation_date)
        print('Modified Date: ', self.modified_date)
        print('Owner: ', self.owner)
        print('Group: ', self.group)
        print('Owner UID: ', self.owner_uid)
        print('Owner GID: ', self.owner_gid)
        print('Permissions: ', self.file_permissions)

"""
    Walk - The cream of the corn
"""
class Walk(object):
    """
        directory (str) - The directory you want to walk
        options (WalkOptions) - Your options 'template'
    """
    def __init__(self, directory, options:WalkOptions):
        self.directory = directory
        self.options = options

    # only print if verbose is enabled
    def vprint(self, text):
        if self.options.verbose:
            print(text)

    def walk(self):
        total_dir_count = 0
        matched_dir_count = 0

        ret_dirs = []

        if os.path.exists(self.directory):
            pass
        else:
            print('[sprint][ERROR]: Directory doesnt exist')

        if os.path.isfile(self.directory):
            print('[sprint][ERROR]: You can only walk directories')
            sys.exit(0)

        # add verbose printing
        self.vprint('[sprint]: Walking directory...')

        for root, directories, files in os.walk(self.directory, topdown=self.options.topdown):
            for name in sorted(directories):
                # print(name)
                total_dir_count = total_dir_count + 1
                full_path = os.path.join(root, name)
                """
                    Here is where the file regex issue lies

                    I think its because use_regex automatically gets turned on when
                    you set your file_regex and its trying to match a NoneType folder
                    regex to directory names
                """
                if self.options.use_regex:
                    if isinstance(self.options.folder_regex, str):
                        folder_regex = re.compile(self.options.folder_regex)
                        folder_regex_match = folder_regex.match(name)
                        if folder_regex_match:
                            abspath = root
                            matched_dir_count = matched_dir_count + 1
                            ret_dirs.append(name)
                    elif isinstance(self.options.folder_regex, list):
                        for regx in self.options.folder_regex:
                            folder_regex = re.compile(regx)
                            folder_regex_match = folder_regex.match(name)
                            if folder_regex_match:
                                abspath = root
                                matched_dir_count = matched_dir_count + 1
                                ret_dirs.append(name)
                    elif self.options.folder_regex is None:
                        ret_dirs.append(name)
                else:
                    abspath = root
                    matched_dir_count = matched_dir_count + 1
                    ret_dirs.append(name)

        self.vprint('[sprint]: Directories: {}'.format(total_dir_count))

        if self.options.folder_regex:
            self.vprint('[sprint] Matched {mdc} directories with -> {r}'.format(mdc=matched_dir_count, r=self.options.folder_regex))

        self.scan_for_files(ret_dirs, self.directory)

    def scan_for_files(self, directories, root): # add verbose printing
        ret_files = []
        total_file_count = 0
        matched_file_count = 0

        self.vprint('\n[sprint]: Scanning for files...')

        for d in directories:
            full_path = os.path.join(root, d)
            if self.options.use_format is False or self.options.use_format is None:
                self.vprint('\n[*]: {}'.format(full_path))

            for name in sorted(os.listdir(full_path)):
                total_file_count = total_file_count + 1
                if isinstance(self.options.file_regex, str):
                    file_regex = re.compile(self.options.file_regex)
                    file_regex_match = file_regex.search(name)
                    if file_regex_match:
                        matched_file_count = matched_file_count + 1
                        file_path = root + '/' + d + '/' + name
                        f = File(file_path)
                        ret_files.append(f)
                        if self.options.use_format is False or self.options.use_format is None:
                            self.vprint('[+--]: {}'.format(f.file_name))
                elif isinstance(self.options.file_regex, list):
                    for regx in self.options.file_regex:
                        file_regex = re.compile(regx)
                        file_regex_match = file_regex.search(name)
                        if file_regex_match:
                            matched_file_count = matched_file_count + 1
                            file_path = root + '/' + d + '/' + name
                            f = File(file_path)
                            ret_files.append(f)
                            if self.options.use_format is False or self.options.use_format is None:
                                self.vprint('[+--]: {}'.format(f.file_name))
                else:
                    file_path = root + '/' + d + '/' + name
                    f = File(file_path)
                    ret_files.append(f)
                    if self.options.use_format is False or self.options.use_format  is None:
                        self.vprint('[+--]: {}'.format(f.file_name))

        self.vprint('\n[sprint] Files: {}'.format(total_file_count))

        if self.options.file_regex:
            self.vprint('[sprint] Matched {mfc} files with -> {r}'.format(mfc=matched_file_count, r=self.options.file_regex))

        if self.options.use_format is None or self.options.use_format is False:
            pass
        else:
            self.format_files(ret_files)

    def format_files(self, files):
        format_count = 0
        # time.sleep(3)
        self.vprint('[sprint] Formating files')
        for f in files:
            file_name = ''
            fn, ext = os.path.splitext(f.file_name)
            if self.options.prefix == 'season+episode':
                episode_regex = [r'(S[0-9])(E[0-9])', r'(S[0-9])\S(E[0-9])\S', r'(s[0-9])(e[0-9])', r'(s\d[0-9])(e\d[0-9])']
                for r in episode_regex:
                    regex = re.compile(r)
                    match = regex.search(f.file_name)
                    if match:
                        file_name = file_name + match.group(0)
                    else:
                        pass
            else:
                file_name = file_name + self.options.prefix

            if self.options.preserve_original_filename: # remove file extension
                original_file_name = f.file_name
                invalid_symbols = ['.', '-', ' ', '\ ']
                if '&' in original_file_name:
                    original_file_name = original_file_name.replace('&', 'and')

                for symbol in invalid_symbols:
                    if symbol in original_file_name:
                        original_file_name = original_file_name.replace(symbol, '_')

                file_name = file_name + '--{}'.format(original_file_name)

            file_name = file_name + ext
            if self.options.dry_run:
                format_count = format_count + 1
                absolute_file_path = f.absolute_path
                path_list = absolute_file_path.split('/')
                path_list.pop(-1)
                full_path = '/Users'
                for element in path_list:
                    if element == '' or '' == element:
                        path_list.remove('')
                    full_path = full_path + element + '/'
                full_path = full_path + file_name
                self.vprint('[sprint][FORMAT]: {ofn} --> {nfn}'.format(ofn=f.file_name, nfn=full_path))
            else:
                absolute_file_path = f.absolute_path
                path_list = absolute_file_path.split('/')
                path_list.pop(-1)
                full_path = '/Users'
                for element in path_list:
                    if element == '' or '' == element:
                        path_list.remove('')
                    full_path = full_path + element + '/'
                full_path = full_path + file_name
                format_count = format_count + 1
                f.chmod(0o100777) # add option for this
                f.rename(full_path)

if __name__ == '__main__':
    # o = WalkOptions()
    # o.set_verbose(True)
    # o.set_dry_run(True)
    # o.set_folder_regex(r'season(\d+)')
    # o.set_prefix('season+episode')
    # w = Walk('/Users/szaluk/media_for_vault/HOW_I_MET_YOUR_MOTHER', o)
    # w.walk()
    f = File('~/Desktop/HOME_ALONE.mkv')
    f.print_info()
