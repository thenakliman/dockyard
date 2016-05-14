# This module does the common tasks required by driver, which are based
# on the bridges concepts. It does following tasks
# 1) Create Virtual Interface # 2) Moving Virtual Interface into docker namespace # 3) Assign IP address to the interface # 4) Brings up network interface

import abc
from network_driver_exceptions import (
    AlreadyInNamespace,
    FailedToMoveInterface,
    InterfaceNotFound,
    InvalidState,
    NamespaceNotFound,
    UnableToAssignIP,
    UnableToChangeState) 
from pyroute2 import IPRoute
from namespace import DockyardNamespace


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


class Addr(object):
    def __init__(self):
        self.ipr = IPRoute()

    def add(self, command, index=None, address=None, mask=None, net_ns_fd=None):
        print command, index, address, mask, net_ns_fd
        self.ipr.addr(command, index=index,
                      address=address, mask=mask,
                      net_ns_fd=net_ns_fd)


class Link(object):
    allowed_states = ['up', 'down']

    def __init__(self):
        self.ipr = IPRoute()

    def add(self, command, ifname, peer, kind='veth'):
        """Create link.
        """
        self.ipr.link(command, 
                      ifname=ifname,
                      kind=kind,
                      peer=peer) 

    # Use decorator to convert net_ns_fd to netns_name
    # currently applying jugad
    def set(self, command,
            index=None, net_ns_fd=None,
            state=None, master=None):
        """Handles links.
        """
        if state:
            self.ipr.link(command,
                          index=index,
                          net_ns_fd = net_ns_fd,
                          state=state)
        else:
            self.ipr.link(command,
                          index=index,
                          net_ns_fd = net_ns_fd,
                          master=master)

    def lookup(self, ifname):
        """Look up all the interfaces.
        """
        return self.ipr.link_lookup(ifname=ifname)


class InterfaceManager(object):
    def __init__(self):
        self.link = Link()
        self.addr = Addr()
        self.netns = DockyardNamespace()

    def _does_if_exist(self, idx):
        """This method checks whether a interface is in the
           namespace.

           idx: index of the network interface
           net_ns_fd: Namespace file descirptor.
 
           It returns True or False, depending on whether interface
           is in namespace or not.
        """

        ifs = self.link.ipr.get_links() 
        ifs_idx = [x['index'] for x in ifs]

        if idx not in ifs_idx:
            return True
        else:
            return False

    def _does_ns_exist(self, net_ns_fd):
        return self.netns.does_exist(net_ns_fd)

    def move_to_namespace(self, idx, net_ns_fd):
        """Moves interface to the namspace.
        """

        if self._does_if_exist(idx):
            msg = ("%s interface does not exist" % (idx))
            raise InterfaceNotFound(msg)

        if not self._does_ns_exist(net_ns_fd):
            try:
                self.netns.attach_namespace(net_ns_fd)
            except:
                msg = ("%s Namespace does not exist" % (idx))
                raise NamespaceNotFound(msg)
            
        #try:
        netns_name = self.netns.get_netns_name(net_ns_fd)
        self.link.set('set', index=idx,
                      net_ns_fd=netns_name)
        #except:
        #    raise FailedToMoveInterface()

    def addr(self, idx, address, mask, broadcast, net_ns_fd):
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
                msg = ("%s Namespace does not exist" % (idx))
                raise NamespaceNotFound(msg)

        try:
            self.addr.add('add', idx,
                          address=address,
                          netmask=mask,
                          broadcast=broadcast,
                          net_ns_fd=net_ns_fd)
        except:
            raise UnableToAssignIP()
      
    def get_index(self, if_name):
        """Get index of the bridge.
        """
        try:
            index = self.link.lookup(ifname=if_name)[0]
        except:
            raise InterfaceNotFound()
       
        return index

    def change_state(self, if_idx, state='up', net_ns_fd=None):
        """Brings interface ups.
        """
        if state not in self.link.allowed_states:
            msg = ("States has to be among %s" % (self.link.allowed_states))
            raise InvalidState(msg)

        try:
            netns_name = self.netns.get_netns_name(net_ns_fd)
            self.link.set(command="set", state=state,
                          index=if_idx, net_ns_fd=netns_name)
        except:
            raise  UnableToChangeState()
