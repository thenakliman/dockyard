from pecan.rest import RestController
from dockyard.engine.controllers.floatingip import FloatingIPController
from dockyard.engine.controllers.interface import InterfaceController

class DockyardNetworkController(RestController):
    """This class expose dockyard network API.
    """
    floatingip = FloatingIPController()
    interface = InterfaceController()

    def __init__(self):
        pass
