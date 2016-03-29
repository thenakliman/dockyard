from dockyard.common import utils, link

import json

class Container(object):
    def __init__(self):
        pass

    def list(self, name_id=None):
        if name_id:
            url = ('/containers/%s/json' % (name_id))
        else:
            url = '/containers/json'
        return utils.dispatch_get_request(url, 'http').data

    def changes(self, name_id=None):
        url = (('/containers/%s/changes') % (name_id))
        return utils.dispatch_get_request(url, 'http').data

    def resize(self, _id, **kwargs):
        url = (('/containers/%s/changes') % (_id))

        if not kwargs:
            query = link.make_query_url(kwargs)
            url = url +'?' + query

        return utils.dispatch_get_request(url, 'http').data

    def export(self, name_id=None):
        url = (('/containers/%s/export') % (name_id))
        return utils.dispatch_get_request(url, 'http').data

    def top(self, name_id=None):
        url = (('/containers/%s/top') % (name_id))
        return utils.dispatch_get_request(url, 'http').data

    def stats(self, _id):
        url = ('/containers/%s/stats' % (_id))
        return utils.dispatch_get_request(url, 'http')

    def archive(self, _id):
        url = ('/containers/%s/archive' % (_id))
        return utils.dispatch_post_request(url, 'http')

    def create(self, body=None):
        url = ('/containers/create')
        return utils.dispatch_post_request(url, 'http', body=json.dumps(body)).data

    def upload(self, _id):
        return "upload"

    def copy(self, _id):
        url = ('/containers/%s/copy' % (_id))
        return utils.dispatch_post_request(url, 'http').data

    def logs(self, _id):
        url = ('/containers/%s/logs' % (_id))
        return utils.dispatch_get_request(url, 'http').data
 
    def start(self, _id):
        url = ('/containers/%s/start' % (_id))
        return utils.dispatch_post_request(url, 'http').data

    def restart(self, _id):
        url = ('/containers/%s/restart' % (_id))
        return utils.dispatch_post_request(url, 'http').data

    def kill(self, _id):
        url = ('/containers/%s/kill' % (_id))
        return utils.dispatch_post_request(url, 'http').data

    def stop(self, _id):
        url = ('/containers/%s/stop' % (_id))
        return utils.dispatch_post_request(url, 'http').data

    def exe(self, _id):
        return "exec"

    def attach(self, _id):
        return "attach" 

    def rename(self, _id, query_params=None):
        url = (('/containers/%s/rename') % (_id))
       
        if query_params:
            query = link.make_query_url(query_params)
            url = url +'?' + query

        return utils.dispatch_post_request(url, 'http').data

    def update(self, _id, body=None):
        url = ('/containers/%s/update' % (_id))
        return utils.dispatch_post_request(url, 'http', body=json.dumps(body)).data

    def pause(self, _id):
        url = ('/containers/%s/pause' % (_id))
        return utils.dispatch_post_request(url, 'http').data

    def unpause(self, _id):
        url = ('/containers/%s/unpause' % (_id))
        return utils.dispatch_post_request(url, 'http').data

    def wait(self, _id):
        url = ('/containers/%s/wait' % (_id))
        return utils.dispatch_post_request(url, 'http').data

    def delete(self, _id):
        url = ('/containers/%s' % (_id))
        return utils.dispatch_delete_request(url, 'http').data
