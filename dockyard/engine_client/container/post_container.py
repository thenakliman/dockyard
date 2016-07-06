from dockyard.common.stores.consul.consul_client import ConsulKV


class PostProcessor(object):
    def __init__(self):
         self.db = ConsulKV()

    def create(self, url, **kwargs):
        """This method does the pre processing required for dockyard functionality.
        """
        
    def list(self, url, **kwargs):
        """This method is list all the containers on different hosts
           as well as one container.
        """
        self.db
