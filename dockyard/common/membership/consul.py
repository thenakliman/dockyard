from consul.Consul import Catalog

from dockyard.common.membership.base import Membership

class Consul(Membership):
    def __init__(self):
        self.catalog = Catalog()

    def get_all_host(self):
        """Returns all the members current agent sees.
        """
        nodes = self.catalog.nodes()
        return nodes
