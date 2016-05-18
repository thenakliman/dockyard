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
    def move_to_namespace(self, if_name, net_ns_fd):
        pass

    @abc.abstractmethod
    def change_state(self, if_name, state):
        pass

    @abc.abstractmethod
    def get_index(self, if_name):
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
        print ifname, net_ns_fd, state
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


class IPManager(object):
    def __init__(self):
        """Manages IP manager.
        """
        self.netns = DockyardNamespace()
        self.addr = Addr()

    def assign_ip(self, ifname, address, mask, broadcast=None, net_ns_fd=None):
        """Assign ip address.
           :ifname: Assign ip address to this interface.
           :address: Assign this ip address.
           :mask: for the network
           :broadcast: broadcast address for the network.
           :net_ns_fd: network file descriptor or namespace.
        """
        netns_name = self.netns.get_netns_name(psid=net_ns_fd)
        self.addr.add(ifname, address, mask, broadcast, net_ns_fd=netns_name)


class InterfaceManager(object):
    def __init__(self):
        self.link = Link()
        self.addr = Addr()
        self.netns = DockyardNamespace()

    def _does_ns_exist(self, net_ns_fd):
        return self.netns.does_exist(net_ns_fd)

    def _does_if_exist(self, if_name):
        return self.link.does_if_exist(if_name)

    def move_to_namespace(self, if_name, net_ns_fd):
        """Moves interface to the namspace.
        """

        if not self._does_if_exist(if_name):
            msg = ("%s interface does not exist" % (if_name))
            raise InterfaceNotFound(msg)

        if not self._does_ns_exist(net_ns_fd):
            try:
                self.netns.attach_namespace(net_ns_fd)
            except:
                msg = ("%s Namespace does not exist" % (if_name))
                raise NamespaceNotFound(msg)
            
        try:
            netns_name = self.netns.get_netns_name(net_ns_fd)
            self.link.move_to_namespace(ifname=if_name,
                                       net_ns_fd=netns_name)
        except:
            raise FailedToMoveInterface()

    def addr(self, if_name, address, mask, broadcast, net_ns_fd):
        """Assign ip address
           idx: Device index
           address: IPv4 or IPv6 address
           mask: address mask
           broadcast: Broadcast address
           net_ns_fd: process id for the container
        """

        if not self._does_ns_exist(net_ns_fd):
            try:
                self.netns.attach_namespace(net_ns_fd)
            except:
                msg = ("%s Namespace does not exist" % (net_ns_fd))
                raise NamespaceNotFound(msg)

        try:
            self.addr.add(if_name=if_name,
                          address=address,
                          netmask=mask,
                          broadcast=broadcast,
                          net_ns_fd=net_ns_fd)
        except:
            raise UnableToAssignIP()
      
    def change_state(self, if_name, state='up', net_ns_fd=None):
        """Brings interface ups.
        """
        if state not in self.link.allowed_states:
            msg = ("States has to be among %s" % (self.link.allowed_states))
            raise InvalidState(msg)

        try:
            netns_name = self.netns.get_netns_name(psid=net_ns_fd)
            self.link.set_state(state=state, ifname=if_name,
                                net_ns_fd=netns_name)
        except:
            raise  UnableToChangeState()

