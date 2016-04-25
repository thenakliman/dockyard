import consul
from oslo_config import cfg

from dockyard.common.membership.base import Membership


CONSUL_SERVICE_OPT = [
    cfg.StrOpt('service_name',
                default='dockyard',
                help='Name of this service used by the consul'),
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='consul',
                         title='Group for the consul parameters')
CONF.register_group(opt_group)
CONF.register_opts(CONSUL_SERVICE_OPT, opt_group)

class Consul(Membership):
    def __init__(self):
#        print help(consul.Consul.Agent.Service.__init__)
        self.service = consul.Consul.Agent.Service(consul.Consul.Agent())
        self.catalog = consul.Consul.Catalog()

    def register(self):
        ip = CONF['default']['host']
        if ip == '0.0.0.0':
            ip = None 

        self.service.register(name=CONF.consul.service_name,
                              address = ip,
                              port = CONF.default.port,
                              tags = CONF.default.agent) 

    def _get_services(self, services):
        return services[1] 

    def get_all_host(self, tag='agent'):
        """Returns all the members current agent sees.
        """
        services = self.catalog.service(CONF.consul.service_name, tag=tag)
        return self._get_services(services)
