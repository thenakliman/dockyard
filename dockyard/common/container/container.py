from dockyard.common import utils, link

import json
from pecan.core import redirect

class Container(object):
    def __init__(self):
        pass

    def list(self, name_id=None, query_params=None):
        if name_id:
            url = ('/containers/%s/json' % (name_id))
        else:
            url = '/containers/json'

        if query_params:
            url = ('%s?%s' % (url, query_params))

        return utils.dispatch_get_request(url, 'http').data

    def changes(self, name_id=None):
        url = (('/containers/%s/changes') % (name_id))
        return utils.dispatch_get_request(url, 'http').data

    def resize(self, _id, **kwargs):
        url = (('/containers/%s/changes') % (_id))

        if kwargs:
            query = link.make_query_url(kwargs)
            url = ('%s?%s' % (url, query ))

        return utils.dispatch_get_request(url, 'http').data

    def export(self, name_id=None):
        url = (('/containers/%s/export') % (name_id))
        redirect(utils.get_link(url, 'http'))
        # return str(utils.dispatch_get_request(url, 'http').data)

    def top(self, name_id=None, query_params=None):
        url = (('/containers/%s/top') % (name_id))

        if query_params:
            url = ('%s?%s' % (url, query_params))

        return utils.dispatch_get_request(url, 'http').data

    def stats(self, _id):
        url = ('/containers/%s/stats' % (_id))
        redirect(utils.get_link(url, 'http'))
        # return utils.dispatch_get_request(url, 'http')

    def archive(self, _id, query_params=None):
        url = ('/containers/%s/archive' % (_id))
        
        if query_params:
            url = ("%s?%s" % (url, query_params))

        #redirect(utils.get_link(url, 'http'))
        return  utils.dispatch_put_request(url, 'http').data

    def create(self, body=None):
        url = ('/containers/create')
        return utils.dispatch_post_request(url, 'http', body=json.dumps(body)).data

    def upload(self, _id, body=None, query_params=None, **kwargs):
        url = ('/containers/%s/archive' %(_id))
        if query_params:
            url = ("%s?%s" % (url, query_params))
 
        return utils.dispatch_put_request(url, 'http', body=body).data

    def copy(self, _id):
        url = ('/containers/%s/copy' % (_id))
        redirect(utils.get_link(url, 'http'))
        # return str(utils.dispatch_post_request(url, 'http').data)

    def logs(self, _id, query_string, **kwargs):
        url = ('/containers/%s/logs?%s' % (_id, query_string))

        if kwargs:
            query = link.make_query_url(kwargs)
            url = url +'/' + query

        redirect(utils.get_link(url, 'http'))
        # return utils.dispatch_get_request(url, 'http').data
 
    def start(self, _id, query_params=None):
        url = ('/containers/%s/start' % (_id))

        if query_params:
            url = ('%s?%s' % (url, query_params))

        return utils.dispatch_post_request(url, 'http').data

    def restart(self, _id, query_params=None):
        url = ('/containers/%s/restart' % (_id))

        if query_params:
            url = ('%s?%s' % (url, query_params))

        return utils.dispatch_post_request(url, 'http').data

    def kill(self, _id, query_params=None):
        url = ('/containers/%s/kill' % (_id))

        if query_params:
            url = ('%s?%s' % (url, query_params))

        return utils.dispatch_post_request(url, 'http').data

    def stop(self, _id, query_params=None):
        url = ('/containers/%s/stop' % (_id))

        if query_params:
            url = ('%s?%s' % (url, query_params))

        return utils.dispatch_post_request(url, 'http').data

    def exe(self, _id):
        abort(404)

    def attach(self, _id, query_params=None):
        url = ('/containers/%s/attach' % (_id))

        if query_params:
            url = ('%s?%s' % (url, query_params))

        redirect(utils.get_link(url, 'http'))

    def rename(self, _id, **kwargs):
        url = (('/containers/%s/rename') % (_id))
       
        if kwargs:
            query = link.make_query_url(kwargs)
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

    def delete(self, _id, **kwargs):
        url = ('/containers/%s' % (_id))

        if kwargs:
            query = link.make_query_url(kwargs)
            url = ('%s?%s' % (url, query))

        return utils.dispatch_delete_request(url, 'http').data
