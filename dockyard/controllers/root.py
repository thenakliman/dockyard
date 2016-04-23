from pecan import expose, rest

from dockyard.controllers import v1


class RootController(rest.RestController):

    _version = ['v1']
    # List of the allowed versions of the API.

    _default_version = 'v1'
    # Default value of the API version.
    v1 = v1.Controller()

    @expose()
    def index(self):
        return "OK\n"

    @expose()
    def _route(self, args):
        """Override default routing.

           It redirect to the default value of the dockyard API, if version
           of the API is not specified or wrongly specified
        """

        if args[0] and args[0] not in self._version:
            args = [self._default_version] + args

        return super(RootController, self)._route(args)
