from pecan import expose
from pecan import rest

from dockyard.common import base
from dockyard.common.information  import information

class Information(rest.RestController):
    def __init__(self):
        self.information = information.Information()

    @expose()
    def get(self):
        return self.information.info()

class Version(rest.RestController):
    def __init__(self):
        self.information = information.Version()

    @expose()
    def get(self):
        return self.information.version()
