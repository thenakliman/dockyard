from pecan import abort
from dockyard.common import link
from dockyard.common import utils, url


class Image(object):
    base_url = '/images'

    def __init__(self):
        self.url = url.URL(self.base_url)

    def list(self, id_=None):
        url_ = self.url.make_url(url_='json', id_=id_)
        return utils.dispatch_get_request(url=url_)

    def history(self, id_=None):
        url_ = self.url.make_url(url_='history', id_=id_)
        return utils.dispatch_get_request(url=url_)

    def search(self, term=None):
        url_ = self.url.make_url(url_='search')
        query = {"term": term}
        return utils.dispatch_get_request(url=url_, query_params=query)

    def create(self, fromImage, tag):
        url_ = self.url.make_url(url_='create')
        query = {"fromImage": fromImage, "tag": tag}
        return utils.dispatch_post_request(url=url_, query_params=query)

    def push(self, _id):
        abort(404)

    def delete(self, id_):
        url_ = self.url.make_url(id_=id_)
        return utils.dispatch_delete_request(url=url_)

    def tag(self, _id=None, **kwargs):
        url_ = self.url.make_url(url_='tag', id_=id_)
        return utils.dispatch_post_request(url=url_, query_params=kwargs)
