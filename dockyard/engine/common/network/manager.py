import importlib
from oslo_config import cfg

from dockyard.engine.common.utils import json_dump, str_to_dict
from dockyard.engine.common.exceptions import InterfaceNotFound

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

        ifs = dict()
        ifs[psid] = self.network.get_ifs(psid)
        return json_dump(ifs)

    def create(self, peer=None, ifname=None, kind='veth'):
        """This method creates interfaces in the namespace.
           :params ifname: Interface name, if not defined random 
                           string will be chossen.
           :params kind: Kind of the veth pair.
           :params peer: peer interface name for this interface.
        """
        ifs_names = dict()
        ifs_names['interface_names'] = \
                   self.network.create_link_pair(ifname=ifname, peer=peer,
                                                 kind=kind)

        return json_dump(ifs_names)

    def update(self, ifname, brname=None, psid=None, state=None):
        """This method is responsible for attaching network interface to
           a bridge or moving an interface to a namespace.
        """
        if brname and psid and state:
            msg = ("Operation not supprted")
            return json_dump(msg)

        data = dict()
        if brname:
            data['port_info'] = self.network.attach_port(ifname=ifname,
                                                         br_name=brname)
        else:
            if psid:
                psid = int(psid)
                try:
                    data["interface_info"] = self.network.move_to_namespace(
                                                     ifname=ifname, psid=psid)
                except:
                    pass

            if state:
                data["state"] = self.network.change_state(ifname=ifname, psid=psid,
                                                          state=state)
             
        return json_dump(data)
