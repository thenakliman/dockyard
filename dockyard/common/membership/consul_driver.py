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
        self.consul = consul.Consul()

    def register(self):
        ip = CONF['default']['host']
        if ip == '0.0.0.0':
            ip = None 

        self.consul.agent.service.register(name=CONF.consul.service_name,
                                           address=ip,
                                           port = CONF.default.port,
                                           tags = ['master']) 

    def _make_dict(self, service):
        print service
        ser = dict()
        info = {
                 'address': service['ServiceAddress'],
                 'port': service['ServicePort']
               } 
        ser[service['Node']] =  info
        return ser;
       
    def _get_services(self, services):
        services_info = []

        for service in services[1]:
            services_info.append(self._make_dict(service))

        return services_info

    def get_all_hosts(self, tag='agent'):
        """Returns all the members current agent sees.
        """
        services = self.consul.catalog.service('dockyard')
        return self._get_services(services)
