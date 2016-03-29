from dockyard.common import utils

import json

class Container(object):
    def __init__(self):
        pass

    def list(self, name_id=None):
        url = '/containers/json'
        return utils.dispatch_get_request(url, 'http').data

    def stats(self, _id):
        url = ('/containers/%s/stats' % (_id))
        return utils.dispatch_get_request(url, 'http')

    def archive(self, _id):
        url = ('/containers/%s/archive' % (_id))
        return utils.dispatch_get_request(url, 'http')

    def create(self, body=None):
        url = ('/containers/create')
        return utils.dispatch_post_request(url, 'http', body=json.dumps(body)).data

    def upload(self, _id):
        return "upload"

    def copy(self, _id):
        return "copy"

    def logs(self, _id):
        url = ('/containers/%s/logs' % (_id))
        return utils.dispatch_get_request(url, 'http')
 
    def start(self, _id):
        return "start"

    def exe(self, _id):
        return "exec"

    def attach(self, _id):
        return "attach" 

    def rename(self, _id):
        return "rename"
