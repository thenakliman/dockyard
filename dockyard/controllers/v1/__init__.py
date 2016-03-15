from  dockyard.controllers.v1 import information
from  dockyard.controllers.v1 import version
from  dockyard.controllers.v1 import container
from  dockyard.controllers.v1 import image
from  dockyard.controllers.v1 import network
from  dockyard.controllers.v1 import volume
	
class Controller(object):
    info = information.Information()
    version = information.Version()
    containers = container.ContainerController()
    images = image.ImageController()
    networks = network.NetworkController()
    volumes = volume.Volumes() 
