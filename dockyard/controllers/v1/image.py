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
    def create(self, *args):
        abort(404)

    @create.when(method="POST")
    def create_POST(self, fromImage, tag='latest'):
        return self.image.create(fromImage, tag).data

    @expose()
    def json(self, _id=None):
        return self.image.list(_id)

class ImageController(object):
    def __init__(self):
        pass

    @expose()
    def _lookup(self, _id, op=None):
        if op != None:
            new_url = (op, _id)
        else:
            new_url = tuple([_id])
        return Image(), new_url;
