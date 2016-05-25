from pecan import expose, abort, request
from pecan.rest import RestController

from dockyard.engine.common.network.manager import NetworkManager

class InterfaceController(RestController):
    def __init__(self):
        self.network = NetworkManager()

    @expose()
    def post(self):
        """This method is responsible for creating network interfaces.
        """
        body = request.body
        return self.network.create(body)
       
    @expose()
    def delete(self):
        pass

    @expose()
    def attach(self):
        pass

    @expose()
    def move(self):
        pass

    @expose()
    def detach(self):
        pass

     # created this for testing purpose only
#    @expose()
    def get_one(self, psid):
        """This method returns networks interfaces in a container.
        """
        return self.network.get_ifs(psid=psid)

class RoutesController(RestController):
    def __init__(self):
        pass

    @expose()
    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

    def get_one(self):
        pass


class IPController(RestController):
    def __init__(self):
        pass

    @expose()
    def put(self):
        pass
 
    @expose()
    def delete(self):
        pass

    @expose()
    def udpate(self):
        pass

    @expose()
    def get_one(self, psid=None):
        """This method returns IPs allocated to a container.
        """
        pass
        

class DockyardEngineController(RestController):
    """Controller for the Engine.
    """

    """This is the controller for the interface.
    """
    interface = InterfaceController()

    """Controller for IPs.
    """
    ip = IPController()

    """Controller for routes.
    """
    routes = RoutesController()

    def __init__(self):
        pass
