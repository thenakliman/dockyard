<<<<<<< Updated upstream
from dockyard.common import base, link
=======
import ast
from pecan import request

>>>>>>> Stashed changes
from dockyard.common import utils

class Network(object):
    def __init__(self):
        pass

    def list(self, name_or_id=None):
        url = '/networks'
        if name_or_id:
            url = url + ('/%s' % (name_or_id))
        return utils.dispatch_get_request(url, 'http').data

    def connect(self, _id):
        url = ('/networks/%s/create' % (_id))
        body = ast.literal_eval(request.environ['webob._parsed_post_vars'][0].keys()[0])
        return utils.dispatch_post_request(url, 'http', body)

    def disconnect(self, _id):
        return "SET network"

    def create(self):
        return "Create Network"
