from pecan import expose

from dockyard.common.volume import volume


class Volume(object):
    def __init__(self):
        self.volume = volume.Volume()

    @expose(generic=True)
    def index(self, name=None):
        return self.volume.list(name)

    @index.when(method='DELETE')
    def index_DELETE(self, name):
        return self.volume.delete(name)

    @expose(generic=True)
    def create(self):
        abort(404)

    @create.when(method='POST')
    def _create(self, **kwargs):
        return self.volume.create(kwargs)


class VolumeController(object):
    def __init__(self):
        pass

    @expose()
    def _lookup(self, op=None):
        new_url = ['']
        if op:
            new_url.append(op)

        if new_url:
            new_url = tuple(new_url)
        else:
            new_url = tuple([''])
        return Volume(), new_url
