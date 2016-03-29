# Pecan Application Configurations
app = {
    'root': 'dockyard.controllers.root.RootController',
    'modules': ['dockyard', 'dockyard.api'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/dockyard/templates',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    },
   'acl_public_routes': [
        '/',
        '/v1',
    ],

}

# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf
