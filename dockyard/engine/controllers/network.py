from dockyard.engine.controllers.floatingip import FloatingIPController
from dockyard.engine.controllers.interface import InterfaceController

class DockyardNetworkController(RestController):
    """This class expose dockyard network API.
    """
    floatingip = FlotingIPController()
    interface = InterfaceController()
