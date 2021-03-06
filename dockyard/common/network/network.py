import json
from pecan import request

from dockyard.common import url, utils


class DockerNetwork(object):
    base_url = '/networks'

    def __init__(self):
        pass

    def list(self, name_or_id=None, host=None):
        url_ = self.url.make_url(id_=name_or_id)
        return utils.dispatch_get_request(url=url_, host=host)

    def connect(self, id_, host=None, **kwargs):
        body = request.body
        url_ = self.url.make_url(url_='connect', id_=id_)
        return utils.dispatch_post_request(url=url_, body=body, host=host)

    def disconnect(self, id_, host=None, **kwargs):
        url_ = self.url.make_url(url_='disconnect', id_=id_)
        body = request.body
        return utils.dispatch_post_request(url=url_, body=body, host=host)

    def create(self, host=None, **kwargs):
        url_ = self.url.make_url(url_='create')
        body = request.body
        return utils.dispatch_post_request(url=url_, body=body, host=host)

    def delete(self, id_, host=None):
        url_ = self.url.make_url(id_=id_)
        return utils.dispatch_delete_request(url=url_, host=host)


class DockyardNetwork(object):
    dockyard_base_url = '/dockyard'

    def __init__(self):
        pass

    def _get_localhost(self):
        return utils.get_localhost()

    def attach_floatingip(self, id_, data):
        """This method attaches floating ip to the containers.
        """
        url_ = self.url.make_dockyard_url(id_=id_, url_='floatingip')
        body = request.body
        return utils.dispatch_post_request(url=url_, body=body,
                                           host=self._get_localhost())


class Network(DockyardNetwork, DockerNetwork):
    def __init__(self):
        super(DockerNetwork, self).__init__()
        super(DockyardNetwork, self).__init__()
        self.url = url.URL(self.base_url, self.dockyard_base_url)
