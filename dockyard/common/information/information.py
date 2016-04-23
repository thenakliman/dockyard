from dockyard.common import base, link
from dockyard.common import utils


class Information(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def info(self):
        host = utils.get_host()
        ln = link.make_url(host=host, protocol='http', url='/info')
        return self.rest_client.GET(ln).data


class Version(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def version(self):
        host = utils.get_host()
        ln = link.make_url(host=host, protocol='http', url='/version')
        return self.rest_client.GET(ln).data
