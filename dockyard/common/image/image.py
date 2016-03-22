from dockyard.common import base, link
from dockyard.common import utils

class Image(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, _id=None):
        return utils.dispatch_request(protocol='http', url='/images/json').data

    def create(self, fromImage, tag):
        query = link.make_query_url(fromImage=fromImage, tag=tag)
        url = (('/images/create?%s') % (query))
        return utils.dispatch_post_request(protocol='http', url=url)

    def push(self, _id):
        return (("PUSH %s Image\n") % (_id))
