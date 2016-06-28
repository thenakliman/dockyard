import consul
import netifaces
from oslo_config import cfg
from oslo_log import log as logging

from dockyard.common.membership.base import Membership
from dockyard.common import exception
from dockyard.common.membership.consul import utils as consul_utils

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


def get_localhost_ip():
    """This method resturns localhost ip.
    """
    ifs = netifaces.interfaces()
    for i in ifs:
        try:
            addr = netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']
        except KeyError:
            pass

        if addr == '127.0.0.1':
            continue

        yield addr

class ConsulHealthCheck(object):
    def __init__(self):
        self.healthy = consul.Consul().health

    def get_healthy_nodes(self, service="dockyard"):
        """Get healthy nodes in the cluster.
        """
        services = self.healthy.service(service=service, passing=True)
        return consul_utils.get_formatted_hosts(services)


class Consul(Membership):
    def __init__(self):
        self.consul = consul.Consul()
        self.healthy_services = ConsulHealthCheck()

    def _register_service(self, name, host, port, tags=None, url=''):
        if not name:
            message = ('Service name to use for registering')
            LOG.exception("Cannot continue, Incomplete info: %s" % message)
            raise exception.IncompleteInfo(message)

        if not port:
            message = ('Port number used by the services to listen')
            LOG.exception("Cannot continue, Incomplete info: %s" % message)
            raise exception.Incompleteinfo(message)
            
        if not host:
            for ip in get_localhost_ip():
                host = ip
                break

        http = ("http://%s:%d/%s" % (host, port, url))
        self.consul.agent.service.register(name=name,
                                           address=host,
                                           port = port,
                                           tags = tags,
                                           http = http,
                                           interval=15) 

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

        self._register_service(name, ip, port, url='images/json')


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
        # services = self.consul.catalog.service('docker')
        services = self.healthy_services.get_healthy_nodes()
        if not services:
            message = "No services are registered to the consul"
            raise exception.NoValidHostFound(message)

        return services
