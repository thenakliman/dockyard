from pecan import expose

from dockyard.common import base
from dockyard.common.information import information


class Information(object):
    def __init__(self):
        self.information = information.Information()

    @expose()
    def info(self):
        return self.information.info()


class Version(object):
    def __init__(self):
        self.information = information.Version()

    @expose()
    def version(self):
        return self.information.version()
