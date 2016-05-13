# This module does the common tasks required by driver, which are based
# on the bridges concepts. It does following tasks
# 1) Create Virtual Interface
# 2) Moving Virtual Interface into docker namespace
# 3) Assign IP address to the interface
# 4) Brings up network interface

import abc
from pyroute2 import IPRoute
from nsenter import Namespace


class BridgeDriversExceptions(Exception):
    pass


class InterfaceNotFound(BridgeDriversExceptions):
    pass


class FailedToMoveInterface(BridgeDriversExceptions):
    pass


class UnableToAssignIP(BridgeDriversExceptions):
    pass


class UnableToChangeState(BridgeDriversExceptions):
    pass


class InvalidState(BridgeDriversExceptions):
    pass


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

    def add(self, command, index=None, address=None, mask=None, **kwargs):
        self.ipr.addr(command, index=index,
                      address=address,
                      mask=mask, **kwargs)


class Link(object):
    __states = ['up', 'down']

    def __init__(self):
        self.ipr = IPRoute()

    def add(self, command, ifname, peer, kind='veth'):
        """Create link.
        """
        self.ipr.link(command, 
                      ifname=ifname,
                      kind=kind,
                      peer=peer) 

    def set(self, command,
            index=None, net_ns_fd=None,
            state=None, master=None):
        """Handles links.
        """
        with Namespace(net_ns_fd, 'net'):
            if state:
                self.ipr.link(command,
                              index=index,
                              state=state)
            else:
                self.ipr.link(command,
                              index=index,
                              master=master)

    def lookup(self, ifname):
        """Look up all the interfaces.
        """
        return self.ipr.link_lookup(ifname=ifname)


class InterfaceManager(object):
    def __init__(self):
        self.link = Link()
        self.addr = Addr()

    def move_to_namespace(self, if_name, net_ns_fd):
        """Moves interface to the namspace.
        """
        idx = self._get_index(if_name)
        try:
            self.link.set('set', index=idx,
                          net_ns_fd=net_ns_fd)
        except:
            raise FailedToMoveInterface()

    def addr(self, address, mask, broadcast, net_ns_fd):
        """Assign ip address
           address: IPv4 or IPv6 address
           mask: address mask
           broadcast: Broadcast address
        """
        try:
            self.addr.add('add', self.int_idx,
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

    def change_state(self, if_name, state='up', net_ns_fd=None):
        """Brings interface ups.
        """

        if state not in self.__states:
            msg = ("States has to be among %s" % (self.__states))
            raise InvalidState(msg)

        idx = self.get_index(if_name)
        try:
            self.link.set(command="set", state=state, index=idx)
        except:
            raise  UnableToChangeState()
        
