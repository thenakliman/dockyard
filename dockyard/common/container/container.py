from dockyard.common import base, link
from dockyard.common import utils

class Container(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, name_id=None):
        host = utils.get_host()
        ln = link.make_url(host=host, protocol='http', url='/containers/json')
        return self.rest_client.GET(ln).data

    def stats(self, _id):
        return "stats"

    def archive(self, _id):
        return "archive"

    def upload(self, _id):
        return "upload"

    def copy(self, _id):
        return "copy"

    def logs(self, _id):
        return "logs"
 
    def start(self, _id):
        return "start"

    def exe(self, _id):
        return "exec"

    def attach(self, _id):
        return "attach" 

    def rename(self, _id):
        return "rename"
