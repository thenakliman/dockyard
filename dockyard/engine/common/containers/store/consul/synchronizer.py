import ast
from oslo_config import cfg

from dockyard.common.container.container import Container
from dockyard.engine.common.containers.store.consul import consul_client


CONF = cfg.CONF


class ContainerSynchronizer(object):
    def __init__(self):
        self.host = {
                      'host': CONF.docker.docker_host,
                      'port': CONF.docker.docker_port
                    }
                     
        self.container = Container()
        self.db = consul_client.ConsulKV()

    def _containers(self):
        """This method fetch all the containers running on local machines.
        """
        containers = self.container.list()
        containers = ast.literal_eval(containers)
        for con in containers:
            yield con


    def synchronize(self):
        """This method is responsible for initilizing databases at the start
           of dockyard. It collects all the containers running on localhost
           and putt the data in the consul
        """
        for container in self._containers():
            self._register(container)

    def _inspect(self, id_):
         return self.container.list(name_or_id=id_, host=self.host)

    def _register(self, container):
        """This method is responsible for registering a container.
        """
        id_ = container["Id"]
        container_info = self.container._inspect(id_=id_)
        print container_info
        self.db.put(id_, container_info)
