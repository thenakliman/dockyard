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


class IFManager(object):
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
        return ifs

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

        return ifs_names

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
             
        return data

class IPManager(object):
    def __init__(self):
        self.ip = class_()

    def addr(self, ifname, address, mask,
             psid, broadcast=None):
        """This method assigns name in the network namespace of container.
           :params ifname: network interface name
           :params address: ip address to be assigned 
           :params mask: netmask for the network
           :params psid: network namespace for the container.
           :params broadcast: broadcast address

           :returns: returns.
        """
        ips = dict()
        ips['IP'] = self.ip.addr(ifname=ifname, address=address,
                                 mask=int(mask), psid=int(psid),
                                 broadcast=broadcast)

        return ips

class RouteManager(object):
    def __init__(self):
        self.route = class_()

    def routes(self, ifname, gateway, psid, dst='default'):
        """Adds route in the given namespace.
           :params oif_name: interface name.
           :params gateway: gateway to be added.
           :params psid: process id of the docker to which gateway
                         has to added.
           :params dst: destinations for the route.
           
           :returns: rotue information.
        """
        routes = dict()
        psid = int(psid)
        routes["routes"] = self.route.add_routes(oif_name=ifname, dst=dst,
                                                 psid=psid, gateway=gateway)

        return routes


class DockyardNetworkManager(object):
    """It handles all the dockyard networking specific settings.
    """
    def __init__(self):
        """Dockyard networking involve playing around with network interfaces
           network routes and ip address.
        """
        self.ip = IPManager()
        self.route = RouteManager()
        self.if_ = IFManager()

    def add_ip(self, ip, gateway, mask, psid):
        """This method uses RouteManages, IPManager, IFManager to perform
           required actions.
          
           :params ip: IP Address to be assigned to the container.
           :params gateway: Gateway to be assigned to the container.
           :params mask: netmask for the network address.
           :params psid: process id for the docker container to which
                         this IP has to be assigned.

           :returns: returns information set to the container.
        """
        # Create network inerfaces.
        ifs = self.if_.create()["interface_names"]

        # Move network interfaces to the namespace
        psid = int(psid)
        self.if_.update(ifname=ifs["int_if"], psid=psid, state="up")

        # Assign IP address to the container
        self.ip.addr(ifname=ifs["int_if"], psid=psid, address=ip,
                      mask=int(mask))

        # Create routes for the newly added interface
        self.route.routes(ifname=ifs["int_if"], psid=psid, gateway=gateway,
                          dst='default')

        return "Gathered Information."
