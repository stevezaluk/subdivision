import os, sys, pwd, grp, time
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
        # self.check_file_existance()
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
