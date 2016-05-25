from pecan import rest
from pecan import expose
from oslo_config import cfg

from dockyard.controllers.v1 import information
from dockyard.controllers.v1 import container
from dockyard.controllers.v1 import image
from dockyard.controllers.v1 import network
from dockyard.controllers.v1 import volume
from dockyard.controllers.v1 import cluster
from dockyard.engine.controllers.network import DockyardEngineController


SERVER_OPT = [
    cfg.BoolOpt('api',
                default='True',
                help=('True for api server, False '
                     'for disabling api server')),
    cfg.BoolOpt('engine',
                default='True',
                help=('True for engine server, '
                      'False for disabling engine server.'))
    ]

CONF = cfg.CONF
CONF.register_opts(SERVER_OPT, group='default')


class Controller(rest.RestController):
    """Controller for both the api server and engine.
    """
    if CONF.default.api:
        info = information.Information()
        version = information.Version()
        containers = container.ContainerController()
        images = image.ImageController()
        networks = network.NetworkController()
        volumes = volume.VolumeController()
        clusters = cluster.ClusterController()

    if CONF.default.engine:
        dockyard = DockyardEngineController()
