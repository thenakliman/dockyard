from dockyard.common import base, link
from dockyard.common import utils

class Network(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, name_or_id):
        host = utils.get_host()
        ln = link.make_url(host=host, protocol='http', url='/networks/')
        return str(self.rest_client.GET(ln).data)

    def set_network(self, _id, *connect):
        return "SET network"

    def create(self, *args):
        return "Create Network"
