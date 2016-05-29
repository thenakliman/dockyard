from pecan import expose, abort, request
from pecan.rest import RestController

from dockyard.engine.common.utils import str_to_dict
from dockyard.engine.common.network.manager import (
    IFManager,
    IPManager,
    RouteManager,
    DockyardNetworkManager)

from dockyard.engine.controllers.utils import do_not_expose

class InterfaceController(RestController):
    def __init__(self):
        self.network = IFManager()

    @do_not_expose
    @expose()
    def post(self):
        """This method is responsible for creating network interfaces.
        """
        kwargs = str_to_dict(request.body)
        return self.network.create(**kwargs)
       
    @do_not_expose
    @expose()
    def delete(self):
        abort(404)

    @do_not_expose
    @expose()
    def put(self):
        kwargs = str_to_dict(request.body)
        return self.network.update(**kwargs)

    @do_not_expose
    @expose()
    def detach(self):
        abort(404)

     # created this for testing purpose only
    @do_not_expose
    @expose()
    def get_one(self, psid):
        """This method returns networks interfaces in a container.
        """
        psid = int(psid)
        return self.network.get_ifs(psid=psid)

class RoutesController(RestController):
    def __init__(self):
        self.routes = RouteManager()

    @do_not_expose
    @expose()
    def delete(self):
        abort(404)

    @do_not_expose
    @expose()
    def post(self):
        kwargs = str_to_dict(request.body)
        return self.routes.routes(**kwargs)

    @do_not_expose
    @expose()
    def get_one(self):
        abort(404)


class IPController(RestController):
    def __init__(self):
        self.ip = IPManager()

    @do_not_expose
    @expose()
    def post(self):
        kwargs = str_to_dict(request.body)
        return self.ip.addr(**kwargs)
 
    @do_not_expose
    @expose()
    def delete(self):
        abort(404)

    @do_not_expose
    @expose()
    def get_one(self, psid=None):
        """This method returns IPs allocated to a container.
        """
        abort(404)


class DockyardNetworkController(RestController):
    """This class expose dockyard network API.
    """
    def __init__(self):
        self.network = DockyardNetworkManager()

    @expose()
    def post(self):
        """It handles floating IP assignment for dockyard containers.
        """
        kwargs = str_to_dict(request.body)
        return self.network.add_ip(**kwargs)


class DockyardEngineController(RestController):
    """Controller for the Engine.
    """

    """This is the controller for the interface.
    """
    interface = InterfaceController()

    """Controller for IPs.
    """
    # ip = IPController()

    """Controller for routes.
    """
    # routes = RoutesController()

    """This controller is for providing dockyard specific networking.
    """
    network = DockyardNetworkController()
 
    def __init__(self):
        pass
