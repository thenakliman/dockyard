from dockyard.common import link
from dockyard.common import utils, url


class Information(object):
    base_url = '/info'

    def __init__(self):
        self.url = url.URL(self.base_url)

    def info(self):
        url_ = self.url.make_url()
        return utils.dispatch_get_request(url_)


class Version(object):
    base_url = '/version'

    def __init__(self):
        self.url = url.URL(self.base_url)

    def version(self):
        url_ = self.url.make_url()
        return utils.dispatch_get_request(url_)
