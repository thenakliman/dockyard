from dockyard.common import base, link
from dockyard.common import utils

class Image(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, _id=None):
        host = utils.get_host()
        ln = link.make_url(host=host, protocol='http', url='/images/json')
        return self.rest_client.GET(ln).data

    def create(self, _id):
        return "Valid create\n"

    def push(self, _id):
        return (("PUSH %s Image\n") % (_id))
