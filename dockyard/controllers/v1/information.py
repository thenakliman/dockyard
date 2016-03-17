from pecan import expose
from pecan import rest

import json

from dockyard.common import base

class Information(rest.RestController):
    @expose()
    def get(self):
        rest_client = base.RESTClient()
        return rest_client.GET('http://10.0.0.12:3333/info').data

class Version(rest.RestController):
    @expose()
    def get(self):
        rest_client = base.RESTClient()
        return rest_client.GET('http://10.0.0.12:3333/version').data
