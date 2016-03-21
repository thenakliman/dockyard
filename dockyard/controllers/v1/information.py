from pecan import expose
from pecan import rest

from dockyard.common import base

class Information(rest.RestController):
    def __init__(self):
        self.rest_client = base.RESTClient()
        super(Information, self).__init__()

    @expose()
    def get(self):
        return self.rest_client.GET('http://127.0.0.1:3333/info').data

class Version(rest.RestController):
    def __init__(self):
        self.rest_client = base.RESTClient()
        super(Version, self).__init__()

    @expose()
    def get(self):
        return self.rest_client.GET('http://127.0.0.1:3333/version').data
