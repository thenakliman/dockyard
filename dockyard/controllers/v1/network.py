from pecan import expose, abort
from pecan.rest import RestController

from dockyard.common.network import network


class NetworkController(RestController):
    def __init__(self):
        self.network = network.Network()

    @expose()
    def post(self, _id, operation=None, **kwargs):
        if not operation:
            operation = _id
            _id = None

        return getattr(self, operation)(_id=_id, **kwargs)

    def create(self, _id=None, **kwargs):
        return self.network.create(**kwargs)

    def connect(self, _id=None, **kwargs):
        return self.network.connect(_id, **kwargs)

    @expose()
    def get_one(self, name_or_id):
        return self.network.list(name_or_id)

    @expose()
    def get(self):
        return self.network.list()

    @expose()
    def delete(self, name_or_id):
        return self.network.delete(name_or_id)

    def disconnect(self, _id, **kwargs):
        return self.network.disconnect(_id, **kwargs)

    def floatingip(self, _id, **kwargs):
        return self.network.attach_floatingip(_id, kwargs)
