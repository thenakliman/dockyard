from pecan import expose, abort
from oslo_config import cfg

from dockyard.common.cluster import cluster

class Cluster(object):
    def __init__(self):
        self.cluster = cluster.Cluster()

    @expose(generic=True)
    def register(self, *args):
        abort(404)

    @register.when(method="PUT")
    def register_POST(self, cluster_id, host_ip, port):
        return self.cluster.register(cluster_id, host_ip, port)
    
    @expose(generic=True)
    def unregister(self, *args):
        abort(404)

    @unregister.when(method="DELETE")
    def unregister_POST(self, cluster_id, host_ip):
        return self.cluster.unregister(cluster_id, host_ip)

class ClusterController(object):
    def __init__(self):
        HOST_SERVICE_OPT = [
            cfg.ListOpt('hosts',
                      default='127.0.0.1:3333',
                      help='Listening address of docker service'),
        ]

        CONF = cfg.CONF
        opt_group = cfg.OptGroup(name='membership',
                                 title='Group for membership of docker services')
        CONF.register_group(opt_group)
        CONF.register_opts(HOST_SERVICE_OPT, opt_group)

    @expose()
    def _lookup(self, op, cluster_id, host_ip, port=None):
       new_url = [op, cluster_id, host_ip]

       if port:
           new_url.append(port)
           
       return Cluster(), tuple(new_url)
