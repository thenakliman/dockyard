from dockyard.common import base, link
from dockyard.common import utils

class Image(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, _id=None):
        return utils.dispatch_get_request(protocol='http', url='/images/json').data

    def create(self, fromImage, tag):
        url = '/images/create'
        query = { "fromImage" : fromImage, "tag" : tag }
        return utils.dispatch_post_request(protocol='http', url=url, query_params=query)

    def push(self, _id):
        return (("PUSH %s Image\n") % (_id))
