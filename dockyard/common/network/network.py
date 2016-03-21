from dockyard.common import base

class Network(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, name_or_id):
        return str(self.rest_client.GET("http://127.0.0.1:3333/networks/").data)

    def set_network(self, _id, *connect):
        return "SET network"

    def create(self, *args):
        return "Create Network"
