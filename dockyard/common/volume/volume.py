import json
from dockyard.common import base, link
from dockyard.common import utils, url


class Volume(object):
    base_url = '/volumes'

    def __init__(self):
        self.url = url.URL(self.base_url)

    def list(self, name=None):
        url_ = self.url.make_url(id_=name)
        return utils.dispatch_get_request(url_)

    def delete(self, name):
        url_ = self.url.make_url(id_=name)
        return utils.dispatch_delete_request(url_)

    def create(self, data):
        url_ = self.url.make_url(url_='create')
        body = json.dumps(data)
        return utils.dispatch_post_request(url, body=body)
