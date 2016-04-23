import json
from dockyard.common import base, link
from dockyard.common import utils


class Volume(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, name=None):
        url = '/volumes'
        if name:
            url = url + ('/%s' % (name))
        return utils.dispatch_get_request(url, 'http').data

    def delete(self, name):
        url = ('/volumes/%s' % (name))
        return utils.dispatch_delete_request(url, 'http').data

    def create(self, data):
        url = '/volumes/create'
        body = json.dumps(data)
        return utils.dispatch_post_request(url, 'http', body=body).data
