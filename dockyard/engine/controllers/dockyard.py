from dockyard.engine.controllers.network import DockyardNetworkController

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
