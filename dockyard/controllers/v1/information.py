from pecan import expose
from pecan.rest import RestController

from dockyard.common.information import information


class Information(RestController):
    def __init__(self):
        self.information = information.Information()

    @expose()
    def get_all(self):
        return self.information.info()


class Version(RestController):
    def __init__(self):
        self.information = information.Version()

    @expose()
    def get_all(self):
        return self.information.version()
