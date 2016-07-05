import ast
import importlib
from oslo_config import cfg
from threading import Thread
import time

from dockyard.common.container.container import Container
from dockyard.common.utils import get_localhost_ip
from dockyard.engine_client.synchronizer.synchronizer import (
    ContainerSynchronizer)

CONF = cfg.CONF


class Synchronizer(Thread):
    def __init__(self):
        if CONF.docker.docker_host == "0.0.0.0":
            for ip in get_localhost_ip():
                host = ip
                break
        else:
            host = CONF.docker.docker_host

        port = CONF.docker.docker_port
        self.host = { 'host': host, 'port': port }
        Thread.__init__(self)
        self.container = Container()
        self.synchronizer = ContainerSynchronizer()
        self.sleep_time = CONF.database.synchronization_time


    def run(self):
        """This thread is responsible for synchronizations of containers,
           and other docker resources.
        """
        while True:
            self._synchronize()
            time.sleep(self.sleep_time)

    def _get_format(self, container):
        """This method converts a container information into the required format
           for the container.
        """
        container_info = {"host": self.host, "Container-Info": container}
        key = (self.host, container["Id"], "container")
        return (key, container_info)


    def _synchronize(self):
        """This method fetch all the containers running on local machines.
        """
        containers = self.container.list(host=self.host)
        containers = containers.replace("null", '"null"')
        containers = ast.literal_eval(containers)

        for con in containers:
            container_info = self._get_format(self._inspect(con))
            self.synchronizer.synchronize([container_info])
            

    def _inspect(self, container):
         container = self.container.list(name_or_id=container["Id"],
                                         host=self.host)

         container = container.replace("null", '"null"')
         container = container.replace("false", '"False"')
         container = container.replace("true", '"True"')
         return ast.literal_eval(container)


def run_synchronizer():
    """This method is responsible for synchronizing containers information
       with the consul databse.
    """ 
    sync = Synchronizer()
    sync.setName("Synchronizer")
    sync.start()

run_synchronizer()
