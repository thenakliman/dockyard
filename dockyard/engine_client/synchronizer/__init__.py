from oslo_config import cfg
from threading import Thread
import time

from synchronizer import ContainerSynchronizer

class Synchronizer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.container = ContainerSynchronizer()
        self.sleep_time = CONF.database.synchronization_time


    def run(self):
        """This thread is responsible for synchronizations of containers,
           and other docker resources.
        """
        while True:
            self.container.synchronize()
            time.sleep(self.sleep_time)


sync = Synchronizer()
sync.setName("Synchronizer")
sync.start()
