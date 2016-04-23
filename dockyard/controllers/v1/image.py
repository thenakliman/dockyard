from pecan import expose, route, abort

from dockyard.common.image import image


class Image(object):
    def __init__(self):
        self.image = image.Image()
        super(Image, self).__init__()

    @expose()
    def push(self, _id):
        return self.image.push(_id)

    @expose(generic=True)
    def index(self):
        abort(404)

    @expose(generic=True)
    def create(self, *args):
        abort(404)

    @create.when(method="POST")
    def create_POST(self, fromImage, tag='latest'):
        return self.image.create(fromImage, tag).data

    @index.when(method="DELETE")
    def delete(self, _id):
        return self.image.delete(_id).data

    @expose()
    def json(self, _id=None):
        return self.image.list(_id)

    @expose()
    def search(self, term=None):
        return self.image.search(term)

    @expose()
    def history(self, _id=None):
        return self.image.history(_id)

    @expose(generic=True)
    def tag(self, *args):
        abort(404)

    @tag.when(method="POST")
    def tag_POST(self, id_or_name, **kwargs):
        return self.image.tag(id_or_name, kwargs).data

    @expose(generic=True)
    def build(self, *args):
        abort(404)

    @build.when(method="POST")
    def build_POST(self, **kwargs):
        return self.image.build(kwargs).data


class ImageController(object):
    def __init__(self):
        pass

    @expose()
    def _lookup(self, _id, op=None):
        if op is not None:
            new_url = (op, _id)
        else:
            new_url = tuple([_id])
        return Image(), new_url
