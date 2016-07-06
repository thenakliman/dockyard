from pecan import abort
from dockyard.common import link
from dockyard.common import utils, url


class Image(object):
    base_url = '/images'

    def __init__(self):
        self.url = url.URL(self.base_url)

    def list(self, id_=None, host=None):
        url_ = self.url.make_url(url_='json', id_=id_)
        return utils.dispatch_get_request(url=url_, host=host)

    def history(self, id_=None, host=None):
        url_ = self.url.make_url(url_='history', id_=id_)
        return utils.dispatch_get_request(url=url_, host=host)

    def search(self, term=None, host=None):
        url_ = self.url.make_url(url_='search')
        query = {"term": term}
        return utils.dispatch_get_request(url=url_, query_params=query,
                                          host=host)

    def create(self, fromImage, tag, host=None):
        url_ = self.url.make_url(url_='create')
        query = {"fromImage": fromImage, "tag": tag}
        return utils.dispatch_post_request(url=url_, query_params=query,
                                           host=host)

    def push(self, _id):
        abort(404)

    def delete(self, id_, host=None):
        url_ = self.url.make_url(id_=id_)
        return utils.dispatch_delete_request(url=url_, host=host)

    def tag(self, _id=None, host=None, **kwargs):
        url_ = self.url.make_url(url_='tag', id_=id_)
        return utils.dispatch_post_request(url=url_, query_params=kwargs,
                                           host=host)
