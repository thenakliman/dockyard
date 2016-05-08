# This module does the common tasks required by driver, which are based
# on the bridges concepts. It does following tasks
# 1) Create Virtual Interface
# 2) Moving Virtual Interface into docker namespace
# 3) Assign IP address to the interface
# 4) Brings up network interface

from pyroute2 import IPRoute

class InsufficientInfo(Exception):
    pass

class InterfaceNotFound(Exception):
    pass

class FailedToMoveInterface(Exception):
    pass

class UnableToAssignIP(Exception):
    pass

class UnableToChangeState(Exception):
    pass

class InterfaceManager(object):
    def __init__(self, id_, bridge=None):
        self.ipr = IPRoute()
        self.id = id_

        if bridge:
            self.bridge = bridge

    def _get_if_name(self, loc, kind='veth'):
        """This method makes name of the interface in the specified format
           for our application.
        """

        if not loc:
            msg = "Location of the interface is not defined"
            raise InsufficientInfo(msg)

        if loc == 'external':
            loc = 'x'
        elif loc == 'internal':
            loc = 'i'

        return ('%s-%s-%s' % (kind, loc, self.id)); 

    def create_link_pair(self, kind='veth', peer=None):
        """Creates links, one for namespace and other out of namespace.
          
           ifname: Name of the interface. In this application, it will
                   contain id of the container, which will be appended
                   to the '[kind]-[i/x]' therefor it produce unique interface
                   name.
           kind:   It is the veth in our application.
           peer:   Name of the peer link, In this application link, out
                   of the namespace contains '[kind]-x-[id]' for external
                   link and '[kind]-i-[id]' for the namespace link.
        """

        self.ext_if = self._get_if_name(loc='external', kind=kind)

        if not peer:
            self.int_if = self._get_if_name(loc='internal', kind=kind)

        try:
            self.ipr.link('add', ifname=self.ext_if,
                          kind=kind,
                          peer=self.int_if) 
        except:
            # A proper exception must be thrown here to inform kind of problem
            # encountered 
            return False

        self.int_idx = self.ipr._get_index(ifname=self.int_if)

        return True

    def move_if(self, net_ns_fd):
        """Moves interface to the namspace.
        """
        try:
            self.ipr.link('set', index=self.int_idx,
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
            self.ipr.addr('add', self.int_idx,
                           address=address,
                           netmask=mask,
                           broadcast=broadcast,
                           net_ns_fd=net_ns_fd)
        except:
            raise UnableToAssignIP()
      
    def _change_state(self, command, state):
        """Change state of the link or attach links.
        """
        try:
            self.ipr.link(command, index=self.int_idx,
                          state=state)
        except:
            raise UnableToChangeState()

    def _get_index(self, ifname):
        """Get index of the bridge.
        """
        try:
            index = self.ipr.link_lookup(ifname=ifname)[0]
        except:
            raise InterfaceNotFound()

        return index

    def up(self, state):
        """Brings interface ups.
        """
        self._change_state(command="set", state="up")

    def down(self, state):
        """Brings interface down.
        """
        self._change_state(command="set", state="down")

    def attach_if(self, master=None):
        """Attach interface to bridges.
        """
        if not master:
            self.master_int_idx = self._get_index(self.bridge)
        else:
            self.master_int_idx = self._get_index(master)
          
        self.ipr.link('set', index=self.int_idx,
                      master=self.master_int_idx)
