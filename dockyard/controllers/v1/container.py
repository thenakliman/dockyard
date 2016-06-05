from pecan import expose, abort, request
from pecan.rest import RestController

from dockyard.common.container import container


class ContainerController(RestController):
    def __init__(self):
        self.container = container.Container()

    def _call_operation(self, name_or_id, operation, **kwargs):
        try:
            return getattr(self, operation)(name_or_id)
        except AttributeError:
            abort(404)

    @expose()
    def get(self, name_or_id, operation, **kwargs):
        return self._call_operation(name_or_id, operation, **kwargs)

    @expose()
    def post(self, name_or_id, operation, **kwargs):
        return self._call_operation(name_or_id, operation, **kwargs)

    @expose()
    def put(self, name_or_id, operation, **kwargs):
        return self._call_operation(name_or_id, operation, **kwargs)

    @expose()
    def delete(self, _id, **kwargs):
        return self.container.delete(_id, **kwargs)

    def resize(self, _id, **kwargs):
        return self.container.resize(_id, **kwargs)

    def changes(self, _id):
        return self.container.changes(_id)

    def export(self, _id):
        return self.container.export(_id)

    def json(self, name_id=None):
        query_params = request.query_string
        return self.container.list(name_id,  query_params=query_params)

    def stats(self, _id):
        return self.container.stats(_id)

    def archive(self, _id):
        query_params = request.query_string
        return self.container.archive(_id, query_params)

    def upload(self, _id, **kwargs):
        body = request.body
        query_params = request.query_string
        return self.container.upload(_id, body=body, query_params=query_params)

    def copy_POST(self, _id):
        return self.container.copy(_id)

    def logs(self, _id):
        query_params = request.query_string
        return self.container.logs(_id, query_params)

    def start(self,  _id):
        query_params = request.query_string
        return self.container.start(_id, query_params=query_params)

    def kill(self,  _id):
        query_params = request.query_string
        return self.container.kill(_id, query_params=query_params)

    def restart(self,  _id):
        return self.container.restart(_id)

    def stop(self,  _id):
        query_params = request.query_string
        return self.container.stop(_id, query_params=query_params)

    def exec_(self, _id):
        return self.container.exe(_id)

    def attach(self, _id):
        query_params = request.query_string
        return self.container.attach(_id, query_params=query_params)

    def rename(self, _id, **kwargs):
        return self.container.rename(_id, **kwargs)

    def top(self, _id):
        query_params = request.query_string
        return self.container.top(_id, query_params=query_params)

    def update(self, _id, **kwargs):
        return self.container.update(_id, kwargs)

    def pause(self, _id):
        return self.container.pause(_id)

    def unpause(self, _id):
        return self.container.unpause(_id)

    def wait(self, _id):
        return self.container.wait(_id)

    def create(self, **args):
        return self.container.create(args)
