from dockyard.common import utils

class Container(object):
    def __init__(self):
        pass

    def list(self, name_id=None):
        return utils.dispatch_get_request('/containers/json', 'http').data

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
