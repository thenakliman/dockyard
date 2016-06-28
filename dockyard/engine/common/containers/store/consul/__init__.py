from oslo_config import cfg
from threading import Thread
import time

from dockyard.engine.common.containers.store.consul.synchronizer import (
    ContainerSynchronizer)

CONSUL_DATABASE_OPT = [
    cfg.IntOpt('synchronization_time',
                default=20,
                help='Time after which data will be synced .'),
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='consul_database',
                         title='Group for the configuration options '
                               'for consul as database.')
CONF.register_group(opt_group)
CONF.register_opts(CONSUL_DATABASE_OPT, opt_group)


class Synchronizer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.container = ContainerSynchronizer()
        self.sleep_time = CONF.consul_database.synchronization_time


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
