import ast, json
from pecan import request

from dockyard.common import utils

class Network(object):
    def __init__(self):
        pass

    def list(self, name_or_id=None):
        url = '/networks'
        if name_or_id:
            url = url + ('/%s' % (name_or_id))
        return utils.dispatch_get_request(url, 'http').data

    def connect(self, _id, data):
        body = json.dumps(data)
        url = ('/networks/%s/connect' % (_id))
        return utils.dispatch_post_request(url, 'http', body=body).data

    def disconnect(self, _id, data):
        body = json.dumps(data)
        url = ('/networks/%s/disconnect' % (_id))
        return utils.dispatch_post_request(url, 'http', body=body).data

    def create(self, data):
        url = ('/networks/create')
        body = json.dumps(data)
        return utils.dispatch_post_request(url, 'http', body=body).data

    def delete(self, _id):
        url = ('/networks/%s' % (_id))
        return utils.dispatch_delete_request(url, 'http').data
