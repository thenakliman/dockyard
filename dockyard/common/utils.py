from oslo_config import cfg

from dockyard.common.container.scheduler.round_robin import RoundRobinScheduler

def get_config(group, option):
    CONF = cfg.CONF
    return CONF.group.option


def get_host():
    return RoundRobinScheduler().get_host()        
