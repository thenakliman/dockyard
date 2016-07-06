from oslo_log import log as logging

from dockyard.common import utils, link
from dockyard.common import url

import json
from pecan.core import redirect

LOG = logging.getLogger(__name__)

class Container(object):
    base_url = '/containers'

    def __init__(self):
        self.url = url.URL(self.base_url)

    def list(self, name_or_id=None, query_params=None, host=None):
        url_ = self.url.make_url(url_='json', id_=name_or_id)

        msg = ("List containers with url: %s "
               "query_params: %s" %
               (url_, query_params))

        LOG.debug(msg)

        return utils.dispatch_get_request(url_, query_params=query_params,
                                          host=host)

    def changes(self, name_or_id=None, host=None):
        url_ = self.url.make_url(url_='changes', id_=name_or_id)
        return utils.dispatch_get_request(url_, host=host)

    def resize(self, id_, host=None, **kwargs):
        url_ = self.url.make_url(url_='resize', id_=id_)

        query = ''
        if kwargs:
            query = link.make_query_url(kwargs)

        return utils.dispatch_get_request(url_, query_params=query, host=host)

    def export(self, name_or_id=None, host=None):
        url_ = self.url.make_url(url_='export', id_=name_or_id)
        redirect(utils.get_link(url_))

    def top(self, name_or_id=None, query_params=None, host=None):
        url_ = self.url.make_url(url_='top', id_=name_or_id)
        return utils.dispatch_get_request(url_, query_params=query_params,
                                          host=host)

    def stats(self, id_, host=None):
        url_ = self.url.make_url(url_='stats', id_=id_)
        redirect(utils.get_link(url_))

    def archive(self, id_, query_params=None, host=None):
        url_ = self.url.make_url(url_='archive', id_=id_)
        return utils.dispatch_put_request(url_, query_params=query_params,
                                          host=host)

    def create(self, body=None, host=None):
        url_ = self.url.make_url(url_='create')
        return utils.dispatch_post_request(url_, body=json.dumps(body),
                                           host=host)

    def upload(self, id_, body=None, query=None, host=None, **kwargs):
        url_ = self.url.make_url(url_='archive', id_=id_)
        return utils.dispatch_put_request(url_, body=body, query_params=query,
                                          host=host)

    def copy(self, id_, host=None):
        url_ = self.url.make_url(url_='copy', id_=id_)
        redirect(utils.get_link(url_, host=host))

    def logs(self, id_, query_string, host=None, **kwargs):
        url_ = self.url.make_url(url_='logs', id_=id_)

        query = ''
        if kwargs:
            query = link.make_query_url(kwargs)

        redirect(utils.get_link(url_, query_params=query))

    def start(self, id_, query_params=None, host=None):
        url_ = self.url.make_url(url_='start', id_=id_)
        return utils.dispatch_post_request(url_, query_params=query_params,
                                           host=host)

    def restart(self, id_, query_params=None, host=None):
        url_ = self.url.make_url(url_='restart', id_=id_)
        return utils.dispatch_post_request(url_, query_params=query_params,
                                           host=host)

    def kill(self, id_, query_params=None, host=None):
        url_ = self.url.make_url(url_='kill', id_=id_)
        return utils.dispatch_post_request(url_, query_params=query_params, host=host)

    def stop(self, id_, query_params=None, host=None):
        url_ = self.url.make_url(url_='stop', id_=id_)
        return utils.dispatch_post_request(url_, query_params=query_params, host=host)

    def exe(self, _id):
        abort(404)

    def attach(self, id_, query_params=None, host=None):
        url_ = self.url.make_url(url_='attach', id_=id_)
        redirect(utils.get_link(url_, quer_params=query_params, host=host))

    def rename(self, id_, host=None, **kwargs):
        url_ = self.url.make_url(url_='rename', id_=id_)

        query = ''
        if kwargs:
            query = link.make_query_url(kwargs)

        return utils.dispatch_post_request(url_, query_params=query, host=host)

    def update(self, id_, body=None, host=None):
        url_ = self.url.make_url(url_='update', id_=id_)
        return utils.dispatch_post_request(url_, body=json.dumps(body), host=host)

    def pause(self, id_, host=None):
        url_ = self.url.make_url(url_='pause', id_=id_)
        return utils.dispatch_post_request(url_, host=host)

    def unpause(self, id_, host=None):
        url_ = self.url.make_url(url_='unpause', id_=id_)
        return utils.dispatch_post_request(url_, host=host)

    def wait(self, id_, host=None):
        url_ = self.url.make_url(url_='wait', id_=id_)
        return utils.dispatch_post_request(url_, host=host)

    def delete(self, id_, host=None, **kwargs):
        url_ = self.url.make_url(id_=id_)

        query = ''
        if kwargs:
            query = link.make_query_url(kwargs)

        return utils.dispatch_delete_request(url_, query_params=query, host=host)
