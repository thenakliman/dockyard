from pecan import expose, abort

from dockyard.common.network import network


class Network(object):
    def __init__(self):
        self.network = network.Network()

    @expose(generic=True)
    def index(self, name_or_id=None):
        return self.network.list(name_or_id)

    @index.when(method="DELETE")
    def index_delete(self, name_or_id):
        return self.network.delete(name_or_id)

    @expose(generic=True)
    def connect(self):
        abort(404)

    @connect.when(method='POST')
    def _connect(self, _id, **kwargs):
        return self.network.connect(_id, kwargs)

    @expose(generic=True)
    def disconnect(self):
        abort(404)

    @disconnect.when(method='POST')
    def _disconnect(self, _id, **kwargs):
        return self.network.disconnect(_id, kwargs)


class NetworkController(object):
    def __init__(self):
        self.network = network.Network()

    @expose(generic=True)
    def create(self):
        abort(404)

    @create.when(method="POST")
    def _create(self, **kwargs):
        return self.network.create(kwargs)

    @expose()
    def _lookup(self, id_name_op=None, op=None):
        new_url = []
        if op:
            new_url.append(op)
            new_url.append(id_name_op)
        elif id_name_op:
            new_url.append('')
            new_url.append(id_name_op)

        if new_url:
            new_url = tuple(new_url)
        else:
            new_url = tuple([''])

        return Network(), new_url
