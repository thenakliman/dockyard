import json
from dockyard.common import link
from dockyard.common import utils, url


class Volume(object):
    base_url = '/volumes'

    def __init__(self):
        self.url = url.URL(self.base_url)

    def list(self, name=None, host=None):
        url_ = self.url.make_url(id_=name)
        return utils.dispatch_get_request(url_, host=host)

    def delete(self, name, host=None):
        url_ = self.url.make_url(id_=name)
        return utils.dispatch_delete_request(url_, host=host)

    def create(self, data, host=None):
        url_ = self.url.make_url(url_='create')
        return utils.dispatch_post_request(url=url_, body=data, host=None)
