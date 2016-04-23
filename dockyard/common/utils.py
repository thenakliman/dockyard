from oslo_config import cfg

from dockyard.common import base, link
from dockyard.common.container.scheduler.round_robin import RoundRobinScheduler

from urllib3 import PoolManager

rest_client = base.RESTClient()


def get_config(group, option):
    CONF = cfg.CONF
    return CONF.group.option


def get_host():
    return RoundRobinScheduler().get_host()


def get_link(url, protocol):
    host = get_host()
    return link.make_url(host=host, protocol=protocol, url=url)


def dispatch_get_request(url, protocol='http', query_params=None):
    ln = get_link(url, protocol)
    pool = PoolManager()

    if query_params:
        query = link.make_query_url(query_params)
        ln = ln + '?' + query

    #return rest_client.GET(ln).data
    return pool.urlopen('GET', url=ln).data


def dispatch_post_request(url, protocol='http', body=None, query_params=None):
    ln = get_link(url, protocol)

    if query_params:
        query = link.make_query_url(query_params)
        ln = ln + '?' + query

    return dispatch_post_req(url=ln, post_params=query_params, body=body).data


def dispatch_put_request(url, protocol='http', body=None, query_params=None):
    ln = get_link(url, protocol)

    if query_params:
        query = link.make_query_url(query_params)
        ln = ln + '?' + query

    return dispatch_put_req(url=ln, post_params=query_params, body=body).data


def dispatch_delete_request(url, protocol='http', query_params=None):
    pool = PoolManager()
    ln = get_link(url, protocol)
    return pool.urlopen('DELETE', url=ln)
    #return rest_client.DELETE(ln).data


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
