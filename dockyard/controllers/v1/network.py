from pecan import expose, abort

from dockyard.common.network import network

class Network(object):
    def __init__(self):
        self.network = network.Network()

    @expose(generic=True)
    def index(self, name_or_id=None):
        return self.network.list(name_or_id)

    @index.when(method='POST')
    def set_network(self, _id, *connect):
        return self.network.set_network(_id, connect)

    @expose(generic=True)
    def create(self):
        abort(404)

    @create.when(method="POST")
    def create(self, *args):
        return self.network.create(args)
    
class NetworkController(object):
    def __init__(self):
        pass

    @expose()
    def _lookup(self, id_name=None, op=None):
        new_url = []

        if op:
            new_url.append([op])

        if id_name:
            new_url.append([id_name])

        if new_url:        
           new_url = tuple(new_url)
        else:
           new_url = tuple([''])  

        return Network(), new_url
