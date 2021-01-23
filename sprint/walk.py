import os, sys, re, time
sys.path.insert(1, '/Users/szaluk/lab/projects/vault_suite/subdivision')
from sprint.file import File
from sprint.options import WalkOptions
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

    @classmethod
    def remove_file_name_from_abspath(self, absolute_path):
        path_list = absolute_path.split('/')
        path_list.pop(-1)
        full_path = '/Users'
        for element in path_list:
            if element == '' or '' == element:
                path_list.remove('')
            full_path = full_path + element + '/'
        # full_path = full_path + file_name

        return full_path

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

        if isinstance(self.options.json, str):
            if os.path.exists(self.options.json) and os.path.isfile(self.options.json):
                self.options.parse_json_options()

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
                    if self.options.full_match:
                        file_regex_match = file_regex.match(name)
                    else:
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
                        if self.options.full_match:
                            file_regex_match = file_regex.match(name)
                        else:
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
                    if self.options.full_match:
                        match = regex.match(f.file_name)
                    else:
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
                full_path = self.remove_file_name_from_abspath(f.absolute_path) + file_name
                self.vprint('[sprint][FORMAT]: {ofn} --> {nfn}'.format(ofn=f.file_name, nfn=full_path))
            else:
                full_path = self.remove_file_name_from_abspath(f.absolute_path) + file_name
                format_count = format_count + 1
                f.chmod(0o100777) # add option for this
                f.rename(full_path)

        if self.options.use_format:
            print('[sprint] Formatted: {} files'.format(format_count))
