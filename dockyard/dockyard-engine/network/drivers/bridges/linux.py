from pyroute2 import IPRoute

from base import InterfaceManager
from network_driver_exceptions import InsufficientInfo 


class LinuxBridgeManager(object):
    def __init__(self):
        self.ln = IPRoute()
        self.if_manager = InterfaceManager()

    def _get_if_name(self, id_, loc, kind='veth'):
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

        return ('%s-%s-%s' % (kind, loc, id_)); 


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

        ext_if = self._get_if_name(id_, loc='external', kind=kind)

        if not peer:
            int_if = self._get_if_name(id_, loc='internal', kind=kind)

        try:
            self.ln.link('add',
                        ifname=ext_if,
                        kind=kind,
                        peer=int_if) 
        except Exception as e:
            # A proper exception must be thrown here to inform kind of problem
            # encountered 
            print e 

        return {'ext_if': ext_if, 'int_if': int_if}

    def attach_if(self, if_ext_idx, master_idx):
        """Attach interface to bridges.
        """
        # Define exception that unable to attach UnableToAttach
        self.ln.link('set', index=if_ext_idx,
                     master=master_idx)

    def move_to_namespace(self, if_name, net_ns_fd):
        self.if_manager.move_to_namespace(if_name, net_ns_fd)

    def addr(self, idx, address, mask, broadcast, net_ns_fd):
        self.if_manager.addr.add(idx, address, mask, broadcast, net_ns_fd)

    def change_state(self, idx, state='up', net_ns_fd=None):
        self.if_manager.change_state(if_name=idx, state=state, net_ns_fd=net_ns_fd)

    def get_index(self, if_name):
        return self.if_manager.get_index(if_name)
