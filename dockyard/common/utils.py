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
    
def dispatch_get_request(url, protocol):
    ln = get_link(url, protocol)
    return rest_client.GET(ln)

def dispatch_post_request(url, protocol, body=None, query_params=None):
    from dockyard.common import stubs
    ln = get_link(url, protocol)
    print body
    return stubs.send_request(ln, body)
#    return rest_client.POST(url=ln, query_params=query_params, body=body)

def dispatch_delete_request(url, protocol, query_params=None):
    ln = get_link(url, protocol)
    return rest_client.DELETE(ln)
