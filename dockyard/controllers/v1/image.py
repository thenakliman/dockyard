from pecan import expose, route
from pecan.rest import RestController

from dockyard.common.image import image


class ImageController(RestController):
    def __init__(self):
        self.image = image.Image()

    @expose()
    def get_one(self, name_or_id, operation):
        if not operation:
            operation = name_or_id
            name_or_id = None

        return getattr(self, operation)(name_or_id)

    @expose()
    # This method is not working, it has to be corrected.
    def get(self, operation):
        return getattr(self, operation)()

    def search(self, term):
        return self.search(term=name_or_id)

    def history(self, name_or_id):
        return self.history(name_or_id)

    def json(self, name_or_id=None):
        return self.list_(_id=name_or_id)

    def push(self, _id):
        return self.image.push(_id)

    @expose()
    def post(self, name=None, operation=None):
        if not operation:
            operation = name_or_id
            name_or_id = None

        return getattr(self, operation)(name_or_id)

    # Test this method
    def create(self, fromImage, tag='latest'):
        return self.image.create(fromImage, tag)

    def tag(self, name, **kwargs):
        return self.image.tag(id_or_name, kwargs)

    # This method has to be put in the misc section, as per API
    # it does not seems to belong to images
    def build(self, **kwargs):
        return self.image.build(kwargs)

    def push(self):
        return self.push(name)

    @expose()
    def delete(self, name):
        return self.image.delete(name)

    def list_(self, _id=None):
        return self.image.list(_id)

    def search(self, term=None):
        return self.image.search(term)

    def history(self, _id=None):
        return self.image.history(_id)
