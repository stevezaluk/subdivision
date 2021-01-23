import json, os

"""
    WalkOptions - A template for the settings
        json (str) - Path to a JSON file
        verbose (bool) - Enable Printing
        topdown (bool) - Walk the directory from the top down
        use_regex (bool) - A bool to determine wether or not to spend time matching file names to a regex
        file_regex (str, list) - The file regex to match against
        folder_regex (str, list) - The directory regex to match against
        full_match (bool) - Fully match all regexs instead of searching in them
        use_format (bool) - A bool to determine wether or not to spend time formating files
        dry_run(bool) - Do everything except formatting
        prefix (str) - Rename each file to start with this. If preserve_original_filename is not turned on. It will rename the file to the prefix
        preserve_original_filename (bool) - Add the original filename to the end of the newly formated file name

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
    def __init__(self, json=None, verbose=None, topdown=None, extensions=None, use_regex=False,
                    file_regex=None, folder_regex=None, full_match=False, use_format=False,
                    dry_run=None, prefix=None, embed_title=None, preserve_original_filename=None):
        self.json = json
        self.verbose = verbose
        self.topdown = topdown
        self.extensions = extensions
        self.use_regex = use_regex
        self.file_regex = file_regex
        self.folder_regex = folder_regex
        self.full_match = full_match
        self.use_format = use_format
        self.dry_run = dry_run
        self.prefix = prefix
        self.embed_title = embed_title
        self.preserve_original_filename = preserve_original_filename

    def parse_json_options(self):
        valid_options_keys = ['verbose', 'topdown', 'file_regex', 'folder_regex', 'full_match', 'dry_run', 'prefix', 'preserve_original_filename']
        possible_dict_keys = ['file_regex', 'folder_regex']
        file = open(self.json, 'r')
        options = json.load(file)

        for option in options:
            key = option
            value = options[option]
            for vok in valid_options_keys:
                if key == vok:
                    if key == 'file_regex' or key == 'folder_regex':
                        ret = []
                        if isinstance(value, dict):
                            for k in value:
                                ret.append(value[k])
                            self.set_variable(key, ret)
                        elif isinstance(value, str):
                            self.set_variable(key, value)
                    else:
                        self.set_variable(key, value)

    ### GETTERS AND SETTERS ###

    def set_variable(self, variable, value):
        if isinstance(variable, str):
            setattr(self, variable, value)
            if variable == 'file_regex' or variable == 'folder_regex':
                self.set_regex(True)
            elif variable == 'prefix' or variable == 'preserve_original_filename':
                self.set_rename(True)
        else:
            print('[sprint][ERROR]: "variable" must be a string')
            sys.exit(0)

    def get_variable(self, variable):
        if isinstance(variable, str):
            return getattr(self, variable)
        else:
            print('[sprint][ERROR]: "variable" must be a string')
            sys.exit(0)

    def set_json(self, j):
        if isinstance(j, str):
            self.json = j
        else:
            print('[sprint][ERROR]: "json" must be a string')
            sys.exit(0)

    def get_json(self):
        return self.json

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

    def set_full_match(self, fm):
        if isinstance(v, bool):
            self.full_match = fm
        else:
            print('[sprint][ERROR]: "full_match" must be a boolean')
            sys.exit(0)

    def get_full_match(self):
        return self.full_match

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
        print(' JSON: ', self.get_json())
        print(' Verbose: ', self.get_verbose())
        print(' Top Down: ', self.get_topdown())
        print(' File Regex: ', self.get_file_regex())
        print(' Folder Regex: ', self.get_folder_regex())
        print(' Full Match: ', self.get_full_match())
        # print(' Perscribed Extensions: ', self.get_extensions())
        print('\n[*] Format Options: ')
        print(' Dry Run: ', self.get_dry_run())
        print(' Prefix: ', self.get_prefix())
        # print(' Embed Title: ', self.get_embed_title())
        print(' Preserve Original Filename: ', self.get_pof())
        print('')
