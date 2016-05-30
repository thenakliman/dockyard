from oslo_config import cfg
from oslo_log import log as logging


class Cluster(object):
    def __init__(self):
        pass

    def register(self, cluster_id, host_ip, port):
        pass

    def unregister(self, cluster_id, host_ip):
        pass

    def get_hosts(self):
        LOG.debug("Registered hosts: %s" % cfg.CONF.membership.hosts)
        return cfg.CONF.membership.hosts
