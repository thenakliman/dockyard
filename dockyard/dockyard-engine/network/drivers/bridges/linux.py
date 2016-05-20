from pyroute2 import IPRoute

from base import InterfaceManager, IPManager
from network_driver_exceptions import (
    InsufficientInfo,
    UnableToCreateInterface)


class LinuxBridgeManager(object):
    def __init__(self):
        self.ln = IPRoute()
        self.if_manager = InterfaceManager()
        self.ip_manager = IPManager()

    def _get_ifname(self, id_, loc, prefix='dockyard'):
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

        return ('%s-%s-%s' % (prefix, loc, id_)); 


    def create_link_pair(self, id_, kind='veth', peer=None):
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

        ext_if = self._get_ifname(id_, loc='external')

        if not peer:
            int_if = self._get_ifname(id_, loc='internal')

        try:
            self.ln.link('add',
                        ifname=ext_if,
                        kind=kind,
                        peer=int_if) 
        except:
            msg = ("Unable to create %s, %s interfaces of %s kind" % (
                   ext_if, int_if, kind))

            raise UnableToCreateInterface(msg)

        return {'ext_if': ext_if, 'int_if': int_if}

    # Make This method working
    def attach_if(self, ifname, br_name):
        """Attach interface to bridges.
        """
        self.ln.link('set', index=ifname,
                     master=br_name)

    def move_to_namespace(self, ifname, psid):
        """move an interface to the docker process namespace.
           :ifname: Interface name
           :psid: Docker processs name.
  
           :raises InterfaceNotFound, NamespaceNotFound, FailedTOMoveInterface
        """

        self.if_manager.move_to_namespace(ifname, psid)

    def addr(self, ifname, address, mask, broadcast=None, psid=None):
        """Assign ip address.
           :ifname: Assign ip address to this interface.
           :address: Assign this ip address.
           :mask: for the network
           :broadcast: broadcast address for the network.
           :net_ns_fd: network file descriptor or namespace.

           :raises NamespaceNotFound, UnableToAssignIP
        """
        self.ip_manager.assign_ip(ifname, address, mask, broadcast, psid)

    def change_state(self, ifname, state='up', psid=None):
        """Change state of the interface.
           :ifname: Interface name
           :state: Expected state of the interface valid values
                   are up, down.
           :psid: process id for the docker container.

           :raises InvalidState, UnableToChangeState
        """
        self.if_manager.change_state(ifname=ifname, state=state, psid=psid)

    def add_routes(self, oif_name, dst='default', gateway='0.0.0.0',
                   psid=None, **kwargs):
        """Add routes to the namespace.
           :dst: destination for which routes are being added.
           :gateway: Gateway to be set.
           :net_ns_fd: Network namespace file descriptor.
           :kwargs: In case of advanced networking, additional parameters
                    might be provided through this option.
        """
        if psid:
            self.if_manager.netns.get_netns_name(psid=psid)

        self.ip_manager.add_routes(oif_name=oif_name, dst=dst, gateway=gateway,
                                   psid=psid, **kwargs)
