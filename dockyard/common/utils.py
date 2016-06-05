import importlib
from oslo_config import cfg
from oslo_log import log as logging
from pecan import request as rcvd_req

from base import DockyardURL
from urllib3 import PoolManager

from dockyard.common import link

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
                default='consul.consul_driver.Consul',
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

request = DockyardURL()

def get_config(group, option):
    CONF = cfg.CONF
    return CONF.group.option


def get_host():
    """This method returns host, for serving the request.

       If this instance of the process is api server then scheduler
       will be used for scheduling host.

       If this instance of the process is engine then it should direct
       to docker procss running on local machine and does preprocessing.
    """
    try:
        rcvd_req.headers.environ['Request-Status']
    except KeyError:
        hosts = membership.get_all_hosts()
        host = scheduler.get_host(hosts=hosts)
    else:
        host = { 'host': CONF['docker_host'], 'port': CONF['docker_port'] }

    return host

def get_localhost():
    d = dict()

    if CONF.default.host == '0.0.0.0':
        d['host'] = '127.0.0.1'
    else:
        d['host'] = CONF.default.host

    d['port'] = CONF.default.port
    return d


def get_link(url, host=None, protocol='http'):
    if not host:
        host = get_host()

    return link.make_url(host=host['host'], port=host['port'], url=url)

def prepare_logging(argv=None):
    """
    log file can be specified as a command line argument
    with key = log-file
    """ 
    if argv is None:
        argv = []

    logging.register_options(CONF)
    CONF(argv[1:], project='dockyard')
    logging.setup(CONF, 'dockyard')

def dispatch_get_request(url, headers=None, protocol='http', query_params=None):
    ln = get_link(url=url, protocol=protocol)

    if query_params:
        query = link.make_query_url(query_params)
        ln = (('%s?%s') % (ln, query))

    return request.send(method='GET', url=ln)


def dispatch_post_request(url, host=None, protocol='http',
                          body=None, query_params=None):

    ln = get_link(host=host, url=url, protocol=protocol)

    if query_params:
        query = link.make_query_url(query_params)
        ln = (('%s?%s') % (ln, query))

    return dispatch_post_req(url=ln, post_params=query_params, body=body)


def dispatch_put_request(url, protocol='http', body=None, query_params=None):
    ln = get_link(url=url, protocol=protocol)

    if query_params:
        query = link.make_query_url(query_params)
        ln = (('%s?%s') % (ln, query))

    return dispatch_put_req(url=ln, post_params=query_params, body=body)


def dispatch_delete_request(url, headers = None, protocol='http',
                            query_params=None):
    ln = get_link(url=url, protocol=protocol)
    return request.send(method='DELETE', url=ln)


def dispatch_post_req(url, headers=None, body=None,
                      post_params=None, host=None):
    if not headers:
        headers = {'Content-Type': 'application/json'}

    return request.send(method='POST', url=url, headers=headers, body=body)


def dispatch_put_req(url, headers=None, body=None, post_params=None):
    if not headers:
        headers = {'Content-Type': 'application/x-tar'}

    return request.send(method='PUT', url=url, headers=headers, body=body)
