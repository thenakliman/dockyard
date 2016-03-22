from oslo_config import cfg

from dockyard.common import base, link
from dockyard.common.container.scheduler.round_robin import RoundRobinScheduler

rest_client = base.RESTClient()

def get_config(group, option):
    CONF = cfg.CONF
    return CONF.group.option

def get_host():
    return RoundRobinScheduler().get_host()        

def get_link(url, protocol):
    host = get_host()
    return link.make_url(host=host, protocol=protocol, url=url)
    
def dispatch_request(url, protocol):
    ln = get_link(url, protocol)
    return rest_client.GET(ln)

def dispatch_post_request(url, protocol):
    ln = get_link(url, protocol)
    return rest_client.POST(ln)
