from dockyard.common import base

class Volume(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, name=None):
        return self.rest_client.GET("http://localhost:3333/volumes").data

    def delete(self, name):
        return "Delete Volume"

    def create(self):
        return "POST create"
