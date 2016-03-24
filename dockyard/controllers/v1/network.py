from pecan import expose, abort

from dockyard.common.network import network

class Network(object):
    def __init__(self):
        self.network = network.Network()

    @expose()
    def index(self, name_or_id=None):
        return self.network.list(name_or_id)

    @expose(generic=True)
    def connect(self):
        abort(404)

    @connect.when(method='POST')
    def _connect(self, _id):
        return self.network.connect(_id)

    @expose(generic=True)
    def disconnect(self):
        abort(404)

    @disconnect.when(method='POST')
    def _disconnect(self, _id):
        return self.network.disconnect(_id)

    @expose(generic=True)
    def create(self):
        abort(404)

    @create.when(method="POST")
    def create(self):
        return self.network.create()
    
class NetworkController(object):
    def __init__(self):
        pass

    @expose()
    def _lookup(self, id_name_op=None, op=None):
        new_url = []

        if op:
            new_url.append(op)
        elif id_name_op:
            new_url.append(id_name_op)

        if op:
            new_url.append(id_name_op)

        if new_url:        
           new_url = tuple(new_url)
        else:
           new_url = tuple([''])  

        print new_url
        return Network(), new_url
