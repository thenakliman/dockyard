# This module is responsible for creating links for the required
# namespace.

import os


class Symlink(object):
    def __init__(self):
        pass

    def create(self, src, dst):
        """This method is responsible for creating symbolic links.
        """
        os.symlink(src, dst)

    def is_symlink(self, path):
        """This method checks whether given path is symlink or not.
        """
        return os.path.islink(path)

    def cleanup(self, path):
        """Remove the file from a path.
           :path: Path of the file to remove.
        """
        os.remove(path)
