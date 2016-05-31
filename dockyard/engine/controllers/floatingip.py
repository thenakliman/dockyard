from pecan import expose, request
from pecan.rest import RestController

from dockyard.engine.common.utils import str_to_dict
from dockyard.engine.common.network.manager import DockyardNetworkManager

class FloatingIPController(RestController):
    def __init__(self):
        self.network = DockyardNetworkManager()

    @expose()
    def post(self, id_):
        """It handles floating IP assignment for dockyard containers.
        """
        kwargs = str_to_dict(request.body)
        return self.network.add_ip(**kwargs)


