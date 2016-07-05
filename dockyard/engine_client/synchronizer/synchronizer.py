import ast
import netifaces
from oslo_config import cfg

from dockyard.engine_client import module, db

CONF = cfg.CONF


class ContainerSynchronizer(object):
    def __init__(self):
        self.db = getattr(module, db)()


    def synchronize(self, containers_info):
        """This method is responsible for initilizing databases at the start
           of dockyard. It collects all the containers running on localhost
           and putt the data in the consul
        """
        for container in containers_info:
            self._register(container)

    def _register(self, container_info):
        """This method is responsible for registering a container.
        """
        (key, container) = container_info
        print container_info
        return self.db.put(str(key), str(container))
