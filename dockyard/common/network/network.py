import json
from pecan import request

from dockyard.common import url, utils


class DockerNetwork(object):
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


class DockyardNetwork(object):
    dockyard_base_url = '/dockyard'
    base_url = '/networks'

    def __init__(self):
        self.url = url.URL(self.base_url)

    def attach_floatingip(self, id_, **kwargs):
        """This method attaches floating ip to the containers.
        """
        url_ = self.url.make_url(id_=id_, url_='/floatingip')
        return utils.dispatch_post_request(url=url_)


class Network(DockerNetwork, DockyardNetwork):
    def __init__(self):
        super(DockerNetwork, self).__init__(self)
        super(DockyardNetwork, self).__init__(self)
