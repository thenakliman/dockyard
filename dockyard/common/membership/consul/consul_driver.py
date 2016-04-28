import consul
from oslo_config import cfg

from dockyard.common.membership.base import Membership

CONF = cfg.CONF


class Consul(Membership):
    def __init__(self):
        self.consul = consul.Consul()

    def _register_service(self, name, host, port, tags=None):
        if not name or not host or not port:
           # raise InsufficientInfo
            pass

        self.consul.agent.service.register(name=name,
                                           address=host,
                                           port = port,
                                           tags = tags) 

    def _register_dockyard(self):
        ip = CONF['default']['host']
        if ip == '0.0.0.0':
            ip = None 
     
        port = CONF['default']['port']
        tags = ['master']
        name = CONF['consul']['service_name']
  
        self._register_service(name, ip, port, tags)

    def _register_docker(self):
        ip = CONF['docker']['docker_host']
        if ip == '0.0.0.0':
            ip = None 
     
        port = CONF['docker']['docker_port']
        name = CONF['docker']['docker_name']
  
        self._register_service(name, ip, port)


    def register(self):
        """ This method registers dockyard service information and
            docker server running on this machine.
        """
        self._register_dockyard()
        self._register_docker()



    def _make_dict(self, service):
        """ This method takes all the information returned by the consul
            and returns ip address and port of the service.
        """

        if service['ServiceAddress']:
            host = service['ServiceAddress']
        else:
            host = service['Address']
        

        info = {
                 'host': host,
                 'port': service['ServicePort']
               } 

        return info;
       
    def _get_services(self, services):
        """ This method returns all the registered services.
        """

        services_info = []

        for service in services[1]:
            services_info.append(self._make_dict(service))
        
        return services_info

    def get_all_hosts(self, tag='agent'):
        """Returns all the members current agent sees.
        """
        services = self.consul.catalog.service('docker')
        return self._get_services(services)
