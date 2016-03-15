from pecan import expose
from pecan import rest


class RootController(object):

    self._version = ['v1.0']
    # List of the allowed versions of the API.

    self._default_version = 'v1.0'
    # Default value of the API version.

    @expose()
    def index(self):
        return dict()

    @expose()
    def _route(self, args):
        """Override default routing.
 
           It redirect to the default value of the dockyard API, if version
           of the API is not specified or wrongly specified
        """

        if args[0] and args[0] not in self._version:
            args = self._default_version + args

        return super(rest.RootController(), self)._route(args) 
