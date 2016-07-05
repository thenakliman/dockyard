import ast
import netifaces
from oslo_config import cfg

from dockyard.engine_client import module, db

CONF = cfg.CONF


class ContainerSynchronizer(object):
    def __init__(self):
        self.db = getattr(module, db)()


    def synchronize(self, infos):
        """This method is responsible for initilizing databases at the start
           of dockyard. It collects all the containers running on localhost
           and putt the data in the consul
        """
        for info in infos:
            self._register(info)

    def _register(self, info):
        """This method is responsible for registering a container.
        """
        (key, value) = info
        return self.db.put(str(key), str(info))
