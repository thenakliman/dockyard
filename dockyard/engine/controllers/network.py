from pecan import expose, abort, request
from pecan.rest import RestController

from dockyard.engine.common.utils import str_to_dict
from dockyard.engine.common.network.manager import IFManager, IPManager

class InterfaceController(RestController):
    def __init__(self):
        self.network = IFManager()

    @expose()
    def post(self):
        """This method is responsible for creating network interfaces.
        """
        kwargs = str_to_dict(request.body)
        return self.network.create(**kwargs)
       
    @expose()
    def delete(self):
        pass

    @expose()
    def put(self):
        kwargs = str_to_dict(request.body)
        return self.network.update(**kwargs)

    @expose()
    def detach(self):
        pass

     # created this for testing purpose only
#    @expose()
    def get_one(self, psid):
        """This method returns networks interfaces in a container.
        """
        psid = int(psid)
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
        self.ip = IPManager()

    @expose()
    def put(self):
        kwargs = str_to_dict(request.body)
        return self.ip.addr(**kwargs)
 
    @expose()
    def delete(self):
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
