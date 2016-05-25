import importlib
import json
from oslo_config import cfg

from dockyard.engine.common.utils import json_dump

CONF = cfg.CONF
# Fetch scheduler defined in the configuration file and load it.
network_driver_info = CONF.default.network_driver
# May be this path can be specified in the configuration file.
network_driver_loc = 'dockyard.engine.common.network.drivers'
network_driver_info = (('%s.%s') % (network_driver_loc, network_driver_info))
module_name, class_name = network_driver_info.rsplit(".", 1)
class_ = getattr(importlib.import_module(module_name), class_name)

class NetworkManager(object):
    """This class acts as middleware between drivers and requests.
    """
    def __init__(self):
        self.network = class_()

    def get_ifs(self, psid):
        """This method returns all the interfaces of the docker container.
           :params psid: process id the container.
                         docker inspect | grep Pid

           :returns: Number of interface in a docker container.
        """
        if not psid:
            msg = ("Invalid namespace, Namespace can not be None.")
            return msg

        psid = int(psid)
        ifs = dict()
        ifs[psid] = self.network.get_ifs(psid)
        return json_dump(ifs)

    def create(self, ifname=None, kind='veth', peer=None):
        """This method creates interfaces in the namespace.
           :params ifname: Interface name, if not defined random 
                           string will be chossen.
           :params kind: Kind of the veth pair.
           :params peer: peer interface name for this interface.
        """
        ifs_names = dict()
        ifs_names['interface_names'] = \
                   self.network.create_link_pair(ifname=ifname,
                                                 kind=kind, peer=peer)

        return json_dump(ifs_names)
        
