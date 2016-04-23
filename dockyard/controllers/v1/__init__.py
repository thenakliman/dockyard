from dockyard.controllers.v1 import information
from dockyard.controllers.v1 import container
from dockyard.controllers.v1 import image
from dockyard.controllers.v1 import network
from dockyard.controllers.v1 import volume
from dockyard.controllers.v1 import cluster
from pecan import rest
from pecan import expose


class Controller(rest.RestController):
    info = information.Information()
    version = information.Version()
    containers = container.ContainerController()
    images = image.ImageController()
    networks = network.NetworkController()
    volumes = volume.VolumeController()
    clusters = cluster.ClusterController()
