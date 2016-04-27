import importlib
from oslo_config import cfg
from urllib3 import PoolManager

from dockyard.common import base, link

SCHEDULER_OPT = [
    cfg.StrOpt('scheduler',
                default='round_robin.RoundRobinScheduler',
                help='Scheduler for the dockyard.'),
    cfg.StrOpt('agent',
                default='master',
                help='Tags to be used.')
]

CONF = cfg.CONF
CONF.register_opts(SCHEDULER_OPT, group='default')

# Fetch scheduler defined in the configuration file and load it.
scheduler_info = CONF.default.scheduler
# May be this path can be specified in the configuration file.
scheduler_loc = 'dockyard.common.container.scheduler'
scheduler_info = (('%s.%s') % (scheduler_loc, scheduler_info))
module_name, class_name = scheduler_info.rsplit(".", 1)
class_ = getattr(importlib.import_module(module_name), class_name)
scheduler = class_()


MEMBERSHIP_OPT = [
    cfg.StrOpt('membership',
                default='consul_driver.Consul',
                help='Scheduler for the dockyard.'),
]

CONF.register_opts(MEMBERSHIP_OPT, group='default')

# Fetch scheduler defined in the configuration file and load it.
membership_info = CONF.default.membership
# May be this path can be specified in the configuration file.
membership_loc = 'dockyard.common.membership'
membership_info = (('%s.%s') % (membership_loc, membership_info))
module_name, class_name = membership_info.rsplit(".", 1)
class_ = getattr(importlib.import_module(module_name), class_name)
membership = class_()
membership.register()


def get_config(group, option):
    CONF = cfg.CONF
    return CONF.group.option


def get_host():
#    print membership.get_all_hosts()
    return scheduler.get_host()


def get_link(url, protocol='http'):
    host = get_host()
    return link.make_url(host=host, protocol=protocol, url=url)


def dispatch_get_request(url, protocol='http', query_params=None):
    ln = get_link(url, protocol)
    pool = PoolManager()

    if query_params:
        query = link.make_query_url(query_params)
        ln = (('%s?%s') % (ln, query))

    return pool.urlopen('GET', url=ln).data


def dispatch_post_request(url, protocol='http', body=None, query_params=None):
    ln = get_link(url, protocol)

    if query_params:
        query = link.make_query_url(query_params)
        ln = (('%s?%s') % (ln, query))

    return dispatch_post_req(url=ln, post_params=query_params, body=body).data


def dispatch_put_request(url, protocol='http', body=None, query_params=None):
    ln = get_link(url, protocol)

    if query_params:
        query = link.make_query_url(query_params)
        ln = (('%s?%s') % (ln, query))

    return dispatch_put_req(url=ln, post_params=query_params, body=body).data


def dispatch_delete_request(url, protocol='http', query_params=None):
    pool = PoolManager()
    ln = get_link(url, protocol)
    return pool.urlopen('DELETE', url=ln)


def dispatch_post_req(url, headers=None, body=None, post_params=None):
    pool = PoolManager()
    if not headers:
        headers = {'Content-Type': 'application/json'}
    return pool.urlopen('POST', url, headers=headers, body=body).data


def dispatch_put_req(url, headers=None, body=None, post_params=None):
    pool = PoolManager()
    if not headers:
        headers = {'Content-Type': 'application/x-tar'}
    return pool.urlopen('PUT', url, headers=headers, body=body).data
