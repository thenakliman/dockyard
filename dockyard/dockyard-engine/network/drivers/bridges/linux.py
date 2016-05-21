from base import InterfaceManager, IPManager, Link
from network_driver_exceptions import (
    InsufficientInfo,
    UnableToAttachPort,
    UnableToCreateInterface)
from utils import RandomNumber


class LinuxBridgeManager(object):
    MAX_IF_LENGTH = 15

    def __init__(self):
        self.link = Link()
        self.if_manager = InterfaceManager()
        self.ip_manager = IPManager()

    def _get_ifname(self, prefix='deth'):
        """This method makes name of the interface in the specified format
           for our application.

           Name returned by this method should not be more than 15 length
           character. 
        """
        
        rand_num = RandomNumber()
        id_ = rand_num.get_number(self.MAX_IF_LENGTH - (len(prefix) + 1))
        return ('%s-%s' % (prefix, id_));


    def create_link_pair(self, ifname=None, kind='veth', peer=None):
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

        if not ifname:
            ext_if = self._get_ifname()
        else:
            ext_if = ifname

        if not peer:
            int_if = self._get_ifname()

        try:
            self.link.create(ifname=ext_if, kind=kind, peer=int_if)
        except Exception as e:
            msg = ("Unable to create %s, %s interfaces of %s kind. ERROR: %s"
                   % (ext_if, int_if, kind, e))

            raise UnableToCreateInterface(msg)

        return {'ext_if': ext_if, 'int_if': int_if}

    # Make This method working
    def attach_port(self, ifname, br_name):
        """Attach interface to bridges.
        """
        try:
            self.link.attach_port(ifname=ifname, bridge=br_name)
        except Exception as e:
            msg = ("Unable to attach %s interface with %s bridge. ERROR: %s"
                    % (ifname, bridge, e))

            raise UnableToAttachPort(msg)

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
