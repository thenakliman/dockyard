from oslo_config import cfg

class Cluster(object):
    def __init__(self):
        pass

    def register(self, cluster_id, host_ip, port):
        pass

    def unregister(self, cluster_id, host_ip):
        pass 

    def get_hosts(self):
        return cfg.CONF.membership.hosts
