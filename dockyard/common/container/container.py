from dockyard.common import base

class Container(object):
    def __init__(self):
        self.rest_client = base.RESTClient()

    def list(self, name_id=None):
        return self.rest_client.GET("http://127.0.0.1:3333/containers/json").data

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
