import json
from pecan import request

from dockyard.common import url, utils


class Network(object):
    base_url = '/networks'

    def __init__(self):
        self.url = url.URL(self.base_url)

    def list(self, name_or_id=None):
        url_ = self.url.make_url(id_=name_or_id)
        return utils.dispatch_get_request(url=url_)

    def connect(self, id_, data):
        body = json.dumps(data)
        url_ = self.url.make_url(url_='connect', id_=id_)
        return utils.dispatch_post_request(url=url_, body=body)

    def disconnect(self, id_, data):
        url_ = self.url.make_url(url_='disconnect', id_=id_)
        body = json.dumps(data)
        return utils.dispatch_post_request(url=url_, body=body)

    def create(self, data):
        url_ = self.url.make_url(url_='create')
        body = json.dumps(data)
        return utils.dispatch_post_request(url=url_, body=body)

    def delete(self, id_):
        url_ = self.url.make_url(id_=id_)
        return utils.dispatch_delete_request(url=url_)
