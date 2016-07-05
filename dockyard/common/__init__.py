import ast
import importlib
from oslo_config import cfg
from threading import Thread
import time 
from dockyard.common.container.container import Container
from dockyard.common.image.image import Image
from dockyard.common.network.network import Network
from dockyard.common.volume.volume import Volume
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
        self.image = Image()
        self.network = Network()
        self.volume = Volume()
        self.synchronizer = ContainerSynchronizer()
        self.sleep_time = CONF.database.synchronization_time


    def run(self):
        """This thread is responsible for synchronizations of containers,
           and other docker resources.
        """
        while True:
            self._synchronize()
            time.sleep(self.sleep_time)

    def _get_format(self, id_, value, type_):
        """This method converts a container information into the required format
           for the container.
        """
        value = {"host": self.host, type_: value}
        key = (self.host["host"], id_, type_)
        return (key, value)
  
    def _synchronize_container(self):
        containers = self.container.list(host=self.host)
        return self._sync(containers, type_="container")

    def _synchronize_image(self):
        images = self.image.list(host=self.host)
        return self._sync(images, type_="image")

    def _synchronize_network(self):
        networks = self.network.list(host=self.host)
        return self._sync(networks, type_="network")

    def _synchronize_volume(self):
        volumes = self.container.list(host=self.host)
        return self._sync(volumes, type_="volume")

    def _sync(self, info_s, type_=None):
        info_s = info_s.replace("null", "None")
        info_s = info_s.replace("true", "True")
        info_s = info_s.replace("false", "False")
        info_s = ast.literal_eval(info_s)
        for info in info_s:
            info = self._get_format(info["Id"], info, type_)
            self.synchronizer.synchronize([info])

    def _synchronize(self):
        """This method fetch all the containers running on local machines.
        """
        self._synchronize_container()
        self._synchronize_volume()
        self._synchronize_image()
        self._synchronize_network()
            

def run_synchronizer():
    """This method is responsible for synchronizing containers information
       with the consul databse.
    """ 
    sync = Synchronizer()
    sync.setName("Synchronizer")
    sync.start()

run_synchronizer()
