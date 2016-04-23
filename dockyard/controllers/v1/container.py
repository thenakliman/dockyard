from pecan import expose, abort, request

from dockyard.common.container import container


class Container(object):
    def __init__(self):
        self.container = container.Container()

    @expose(generic=True)
    def index(self):
        abort(404)

    @index.when(method="DELETE")
    def delete(self, _id, **kwargs):
        return self.container.delete(_id, **kwargs)

    @expose(generic=True)
    def resize(self, _id, **kwargs):
        abort(404)

    @resize.when(method="POST")
    def resize_(self, _id, **kwargs):
        return self.container.resize(_id, **kwargs)

    @expose()
    def changes(self, _id):
        return self.container.changes(_id)

    @expose()
    def export(self, _id):
        return self.container.export(_id)

    @expose()
    def json(self, name_id=None):
        query_params = request.query_string
        return self.container.list(name_id,  query_params=query_params)

    @expose()
    def stats(self, _id):
        return self.container.stats(_id)

    @expose(generic=True)
    def archive(self, _id):
        query_params = request.query_string
        return self.container.archive(_id, query_params)

    @archive.when(method="PUT")
    def upload(self, _id, **kwargs):
        body = request.body
        query_params = request.query_string
        return self.container.upload(_id, body=body, query_params=query_params)

    @expose(generic=True)
    def copy(self, _id):
        abort(404)

    @copy.when(method="POST")
    def copy_POST(self, _id):
        return self.container.copy(_id)

    @expose(generic=True)
    def logs(self, _id):
        query_params = request.query_string
        return self.container.logs(_id, query_params)

    @expose(generic=True)
    def start(self):
        abort(404)

    @start.when(method="POST")
    def start_POST(self,  _id):
        query_params = request.query_string
        return self.container.start(_id, query_params=query_params)

    @expose(generic=True)
    def kill(self):
        abort(404)

    @kill.when(method="POST")
    def kill_POST(self,  _id):
        query_params = request.query_string
        return self.container.kill(_id, query_params=query_params)

    @expose(generic=True)
    def restart(self):
        abort(404)

    @restart.when(method="POST")
    def restart_POST(self,  _id):
        return self.container.restart(_id)

    @expose(generic=True)
    def stop(self):
        abort(404)

    @stop.when(method="POST")
    def stop_POST(self,  _id):
        query_params = request.query_string
        return self.container.stop(_id, query_params=query_params)

    @expose(generic=True, route='exec')
    def exe(self):
        abort(404)

    @exe.when(method="POST")
    def exec_POST(self, _id):
        return self.container.exe(_id)

    @expose(generic=True)
    def attach(self):
        abort(404)

    @attach.when(method="POST")
    def attach_POST(self, _id):
        query_params = request.query_string
        return self.container.attach(_id, query_params=query_params)

    @expose(generic=True)
    def rename(self):
        abort(404)

    @rename.when(method="POST")
    def rename_POST(self, _id, **kwargs):
        return self.container.rename(_id, **kwargs)

    @expose()
    def top(self, _id):
        query_params = request.query_string
        return self.container.top(_id, query_params=query_params)

    @expose(generic=True)
    def update(self, _id):
        abort(404)

    @update.when(method="POST")
    def update_POST(self, _id, **kwargs):
        return self.container.update(_id, kwargs)

    @expose(generic=True)
    def pause(self, _id):
        abort(404)

    @pause.when(method="POST")
    def pause_POST(self, _id):
        return self.container.pause(_id)

    @expose(generic=True)
    def unpause(self, _id):
        abort(404)

    @unpause.when(method="POST")
    def unpause_POST(self, _id):
        return self.container.unpause(_id)

    @expose(generic=True)
    def wait(self, _id):
        abort(404)

    @wait.when(method="POST")
    def wait_POST(self, _id):
        return self.container.wait(_id)

    def delete(self, _id):
        return self.container.delete(_id)


class ContainerController(object):
    def __init__(self):
        pass

    @expose(generic=True)
    def create(self, *args):
        abort(404)

    @create.when(method="POST")
    def create_container(self, **args):
        return container.Container().create(args)

    @expose()
    def json(self):
        return Container().json()

    @expose(generic=True)
    def index(self):
        abort(404)

    @expose()
    def index_DELETE(self, _id, **kwargs):
        Container().delete(_id, **kwargs)

    @expose()
    def _lookup(self, id_name_op=None, op=None, *args):
        new_url = []
        if op:
            new_url.append(op)
        elif id_name_op:
            new_url.append(id_name_op)

        if op:
            new_url.append(id_name_op)

        if args:
            new_url.append(args)

        if new_url:
            new_url = tuple(new_url)
        else:
            new_url = tuple([''])

        return Container(), new_url
