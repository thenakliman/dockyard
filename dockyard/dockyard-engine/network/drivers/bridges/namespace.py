# This module is responsible for making namespace descriptor to be
# present in /var/run/netns/.

from network_driver_exceptions import UnableToAttachNamespace
from symlink import Symlink

class Namespace(object):
    def __init__(self):
        pass

class DockyardNamespace(Namespace):
    _DOCKYARD_BASE_NETNS = "/var/run/dockyard/%d/ns/net"
    _BASE_NETNS = "/var/run/netns"

    def __init__(self):
        self.symlink = Symlink()

    def __attach_namespace(self, src, dst):
        """This method attach to existing namespace.
           src: It is the location of the file descriptor of the
                namespace to attach.
           dst: It is the location, where new file descriptor will be
                created.
        """
        try:
            self.symlink.create(src, dst)
        except:
            msg = ("Unable to attach to docker namespace")
            raise UnableToAttachNamespace(msg)
     
    def _get_src_netns(self, psid):
        """This method return the orignial network namespace for
           a docker container.
        """
        path = ("/proc/%d/ns/net" % (psid))
        return path

    def _get_netns_loc(self, psid):
        """Get network namespace location for the dockyard.
        """
        return ("%s/dockyard_%d" % (self._BASE_NETNS, psid))

    def attach_netns_namespace(self, psid):
        """This method creates namespace for the pyroute library.
        """
        src_netns = self._get_src_netns(psid)
        dst_netns = ("%s/%s" % (self._BASE_NETNS, self.get_netns_name(psid)))
        self.__attach_namespace(src_netns, dst_netns)

    def attach_dockyard_namespace(self, psid):
        """This method creates namespace for the dockyard.
        """
        src_netns = self._get_src_netns(psid)
        dst_netns = self._get_netns_loc(psid)
        self.__attach_namespace(src_netns, dst_netns)

    def attach_namespace(self, psid):
        """Attach network namespace for dockyard.
        """
        self.attach_netns_namespace(psid)

    def does_exist(self, psid):
        """Checks whether network namespace exist or not.
        """
        path = self._get_netns_loc(psid)
        return self.symlink.is_symlink(path)

    def get_netns_name(self, psid):
        """Returns name of the namespace.
        """ 
        netns_name = ("dockyard_%d" % (psid))
        return netns_name
