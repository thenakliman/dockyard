from oslo_config import cfg

from dockyard.common.cluster import cluster
from dockyard.common.container.scheduler.base import Scheduler


class RoundRobinScheduler(Scheduler):
    count = -1

    def __init__(self):
        self.cluster = cluster.Cluster()

    def get_host(self):
        hosts = self.cluster.get_hosts()
        num_hosts = len(hosts)
        self.count = (self.count + 1) % num_hosts
        return (hosts[self.count])
