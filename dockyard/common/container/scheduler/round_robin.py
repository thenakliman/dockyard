from oslo_config import cfg

from dockyard.common.container.scheduler.base import Scheduler


class RoundRobinScheduler(Scheduler):
    count = -1

    def __init__(self):
        pass

    def get_host(self, hosts):
        num_hosts = len(hosts)
        self.count = (self.count + 1) % num_hosts
        return (hosts[self.count])
