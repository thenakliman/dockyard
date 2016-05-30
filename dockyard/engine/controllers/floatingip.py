from dockyard.engine.common.network.manager import DockyardNetworkManager

class FloatingIPController(object):
    def __init__(self):
        self.network = DockyardNetworkManager()

    @expose()
    def post(self):
        """It handles floating IP assignment for dockyard containers.
        """
        kwargs = str_to_dict(request.body)
        return self.network.add_ip(**kwargs)


