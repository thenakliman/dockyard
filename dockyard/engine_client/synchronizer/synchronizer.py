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
            self._sync(info)

    def _get_value(self, key):
        """This method returns all the values corresponding to a
           key and resturn.
        """
        return self.db.get(key)

    def _sync(self, info):
        """This method is responsible for registering a container.
        """
        (key, value) = info
        return self.db.put(str(key), str(value))
