# This module does the common tasks required by driver, which are based
# on the bridges concepts. It does following tasks
# 1) Create Virtual Interface # 2) Moving Virtual Interface into docker namespace # 3) Assign IP address to the interface # 4) Brings up network interface

import abc
from network_driver_exceptions import (
    AlreadyInNamespace, FailedToMoveInterface,
    InterfaceNotFound,
    InvalidState,
    NamespaceNotFound,
    UnableToAssignIP,
    UnableToAddRoutes,
    UnableToChangeState) 

from pyroute2 import IPDB, NetNS
from namespace import DockyardNamespace

# make sure this files interfaces are updated as per
# changes.
class BridgeManager(object):
    def __init__(self):
        pass

    @abc.abstractmethod
    def create_link_pair(self, kind, peer=None):
        pass

    @abc.abstractmethod
    def attach_if(self, master, bridge):
        pass

    @abc.abstractmethod
    def addr(self, address, mask, broadcast, net_ns_fd):
        pass
 
    @abc.abstractmethod
    def move_to_namespace(self, ifname, net_ns_fd):
        pass

    @abc.abstractmethod
    def change_state(self, ifname, state):
        pass

    @abc.abstractmethod
    def get_index(self, ifname):
        pass


class IPDBManager(object):
    def __init__(self):
        pass

    def open_ipdb(self, net_ns_fd=None):
        self.ns = None

        if net_ns_fd:
            self.ns = NetNS(net_ns_fd) 
            ipdb = IPDB(nl=self.ns)
        else:
            ipdb = IPDB()

        return ipdb
    

    def close_ipdb(self, ipdb):
        if self.ns:
            self.ns.close()
        
        ipdb.commit()
        ipdb.release()


class Addr(object):
    def __init__(self):
        self.ipdb_manager = IPDBManager()

    def add(self, ifname=None, address=None,
            mask=None, broadcast=None, net_ns_fd=None):
        """Add ip address to the interface in namespace or outside
           the name space.
        """
        ipdb = self.ipdb_manager.open_ipdb(net_ns_fd=net_ns_fd)

        if address:
            address = ("%s/%d" % (address, mask))

        with ipdb.interfaces[ifname] as interface:
            if address:
                interface.add_ip(address)

        self.ipdb_manager.close_ipdb(ipdb)

    def routes(self, dst, gateway, oif, net_ns_fd=None, **kwargs):
        """Add routes to the namespace.
           :dst: destination for which routes are being added.
           :gateway: Gateway to be set.
           :net_ns_fd: Network namespace file descriptor.
           :kwargs: In case of advanced networking, additional parameters
                    might be provided through this option.
        """
        ipdb = self.ipdb_manager.open_ipdb(net_ns_fd=net_ns_fd)
        t = {}
        t['dst'] = dst
        t['gateway'] = gateway
        t['oif'] = oif

        specs = t.copy()
        specs.update(kwargs)

        with ipdb.routes[dst] as route:
            for key, value in specs.iteritems():
                if value == dst:
                    continue
                route[key] = value

        self.ipdb_manager.close_ipdb(ipdb)


class Link(object):
    allowed_states = ['up', 'down']

    def __init__(self):
        self.ipdb_manager = IPDBManager()

    def create(self, ifname, peer, kind='veth', net_ns_fd=None):
        """Create link.
        """
        ipdb = self.ipdb_manager.open_ipdb(net_ns_fd) 
        ipdb.create(ifname=ifname, kind=kind, peer=peer)
        self.ipdb_manager.close_ipdb(ipdb)
        
    def move_to_namespace(self, ifname, net_ns_fd):
        """Move an interface to the namespace.
        """
        ipdb = self.ipdb_manager.open_ipdb() 

        with ipdb.interfaces[ifname] as interface:
            interface.net_ns_fd = net_ns_fd

        self.ipdb_manager.close_ipdb(ipdb)

    def set_state(self, ifname, net_ns_fd=None, state=None):
        """Set state of the interface up/down in the namespace.
        """
        ipdb = self.ipdb_manager.open_ipdb(net_ns_fd) 

        with ipdb.interfaces[ifname] as interface:
            getattr(interface, state)()
        
        self.ipdb_manager.close_ipdb(ipdb)
        
    def get_ifs(self, net_ns_fd=None):
        """Look up all the interfaces.
        """
        ipdb = self.ipdb_manager.open_ipdb(net_ns_fd) 
        ifs = [x for x in ipdb.interfaces if isinstance(x, str)]
        self.ipdb_manager.close_ipdb(ipdb)
        return ifs

    def get_if(self, name, net_ns_fd=None):
        """Look up all the interfaces.
        """
        ipdb = self.ipdb_manager.open_ipdb(net_ns_fd) 
        if_info = ipdb.interfaces[name]
        self.ipdb_manager.close_ipdb(ipdb)
        return if_info

    def does_if_exist(self, ifname, net_ns_fd=None):
        """This method checks whether a interface is in the
           namespace.

           ifname: interface name of the network interface
           net_ns_fd: Namespace file descirptor.
 
           It returns True or False, depending on whether interface
           is in namespace or not.
        """

        ipdb = self.ipdb_manager.open_ipdb(net_ns_fd) 
        try:
            ipdb.interfaces[ifname]
        except:
            return False
        else:
            self.ipdb_manager.close_ipdb(ipdb)

        return True

    def attach_port(self, ifname, bridge, net_ns_fd=None):
        """This method attach interface to the bridge.
           :ifname: interface name to attach to the bridge.
           :bridge: Name of the bridge to which attach interface.
        """
        ipdb = self.ipdb_manager.open_ipdb(net_ns_fd=net_ns_fd)

        with ipdb.interfaces[bridge] as br:
            br.add_port(ipdb.interfaces[ifname])

        self.ipdb_manager.close_ipdb(ipdb)


class IPManager(object):
    def __init__(self):
        """Manages IP manager.
        """
        self.netns = DockyardNamespace()
        self.addr = Addr()
        self.link = Link()

    def _does_ns_exist(self, psid):
        return self.netns.does_exist(psid)

    def _check_and_attach(self, psid):
        if not self._does_ns_exist(psid):
            try:
                self.netns.attach_namespace(psid)
            except Exception as e:
                msg = ("%s Namespace does not exist. ERROR: %s" % (psid, e))
                raise NamespaceNotFound(msg)

        return psid

    def assign_ip(self, ifname, address, mask, broadcast=None, psid=None):
        """Assign ip address.
           :ifname: Assign ip address to this interface.
           :address: Assign this ip address.
           :mask: for the network
           :broadcast: broadcast address for the network.
           :net_ns_fd: network file descriptor or namespace.

           :raises NamespaceNotFound, UnableToAssignIP
        """
        netns_name = None

        if psid:
            psid = self._check_and_attach(psid)
            netns_name = self.netns.get_netns_name(psid=psid)

        try:
            self.addr.add(ifname, address, mask,
                          broadcast, net_ns_fd=netns_name)
        except Exception as e:
            msg = ("Unable to assign ip %s to %s interface in psid namespace."
                   "ERROR: %s" % (address, ifname, psid, e))

            raise UnableToAssignIP(msg)

    def add_routes(self, dst, gateway, oif_name, psid=None, **kwargs):
        """Add routes to the namespace.
           :dst: destination for which routes are being added.
           :gateway: Gateway to be set.
           :net_ns_fd: Network namespace file descriptor.
           :kwargs: In case of advanced networking, additional parameters
                    might be provided through this option.
        """
        netns_name = None

        if psid:
            psid = self._check_and_attach(psid)
            netns_name = self.netns.get_netns_name(psid=psid)

        if self.link.does_if_exist(oif_name, net_ns_fd=netns_name):
            oif_idx = self.link.get_if(oif_name, net_ns_fd=netns_name)
            oif_idx = oif_idx['index']
        else:
            msg = ("%s interface for setting default route in %s namespace "
                   "is not found" % (oif_name, netns_name))

            raise InterfaceNotFound(msg)

        try:
            if netns_name:
                self.addr.routes(oif=oif_idx, dst=dst, gateway=gateway,
                                 net_ns_fd=netns_name, **kwargs)
            else:
                self.addr.routes(oif=oif_idx, dst=dst,
                                 gateway=gateway, **kwargs)
        except Exception as e:
            msg = ("Unable to add gateway %s for destination %s in namespace "
                   "%s for interface %d. ERROR: %s" % (gateway, dst,
                                                       netns_name, oif_idx, e))

            raise UnableToAddRoutes(msg)


class InterfaceManager(object):
    def __init__(self):
        self.link = Link()
        self.netns = DockyardNamespace()

    def _does_ns_exist(self, psid):
        return self.netns.does_exist(psid)

    def _does_if_exist(self, ifname, psid=None):
        """Checks whether interface exist or not in a namespace.
           :ifname: Name of the interface.
           :psid: process id of the container.
  
           :returns True or False based on whether ifname exist or not.
        """
        ns = False

        if not psid:
            ns = self.link.does_if_exist(ifname)
        else:
            netns_name = self.netns.get_netns_name(ifname, psid)
            ns = self.link.does_if_exist(ifname, net_ns_fd=netns_name)
  
        return ns

    def move_to_namespace(self, ifname, psid):
        """Moves interface to the namspace.
           :ifname: Interface name.
           :psid: Process id for the docker container.

           :raises NamespaceNotFound, FailedToMoveInterface
        """

        if not self._does_if_exist(ifname):
            msg = ("%s interface does not exist" % (ifname))
            raise InterfaceNotFound(msg)

        if not self._does_ns_exist(psid):
            try:
                self.netns.attach_namespace(psid)
            except Exception as e:
                msg = ("%s Namespace does not exist. ERROR: %s" % (ifname, e))
                raise NamespaceNotFound(msg)
            
        try:
            netns_name = self.netns.get_netns_name(psid)
            self.link.move_to_namespace(ifname=ifname,
                                        net_ns_fd=netns_name)
        except Exception as e:
            msg = ("Failed to move %s interface in %s namespace. ERROR: %s" % (
                   ifname, netns_name, e))

            raise FailedToMoveInterface(msg)

    def change_state(self, ifname, state='up', psid=None):
        """Brings interface ups.
           :ifname: Interface name
           :state: Expected state of the interface.
           :psid: Process id of the docker process.

           :raises InvalidState, UnableToChangeState
        """
        if state not in self.link.allowed_states:
            msg = ("States has to be among %s but Received %s state" % (
                   self.link.allowed_states, state))

            raise InvalidState(msg)

        if psid:
            netns_name = self.netns.get_netns_name(psid=psid)
        else:
            netns_name = None

        try:
            self.link.set_state(state=state, ifname=ifname,
                                net_ns_fd=netns_name)
        except Exception as e:
            msg = ("Unable to change state of %s interface to %s state in "
                   "%s namespace.ERROR: %s" % (ifname, state, net_ns_fd, e))

            raise  UnableToChangeState(msg)
