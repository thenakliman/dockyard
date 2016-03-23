from dockyard.common import base, link
from dockyard.common import utils

class Volume(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, name=None):
    	host = utils.get_host()
        ln = link.make_url(host=host, protocol='http', url='/volumes')
        return self.rest_client.GET(ln).data

    def delete(self, name):
        return "Delete Volume"

    def create(self):
        return "POST create"
