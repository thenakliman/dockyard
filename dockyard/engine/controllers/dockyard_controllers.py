from pecan.rest import RestController
from dockyard.engine.controllers.network import DockyardNetworkController
from dockyard.engine.controllers.interface import InterfaceController

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
    networks = DockyardNetworkController()
 
    def __init__(self):
        pass
