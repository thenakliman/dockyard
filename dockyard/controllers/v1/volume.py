from pecan import expose, request
from pecan.rest import RestController

from dockyard.common.volume import volume

class VolumeController(RestController):
    """This class exposes all the API's related with volume.
    """
    def __init__(self):
        self.volume = volume.Volume()

    @expose()
    def get_one(self, name=None):
        return self.volume.list(name=name)

    @expose()
    def get(self):
        return self.volume.list()

    @expose()
    def delete(self, name):
        return self.volume.delete(name=name)

    @expose()
    def post(self, operation=None):
        body = request.body
        return self.volume.create(data=body)
