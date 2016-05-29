from oslo_log import log as logging

from pecan import expose, rest, request

from dockyard.controllers import v1

LOG = logging.getLogger(__name__)

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

        if request.body:
            msg = ("Processing request: url: %(url)s, "
                   "method: %(method)s, "
                   "body: %(body)s" %
                   {'url': request.url,
                    'method': request.method,
                    'body': request.body})
            LOG.debug(msg)
        return super(RootController, self)._route(args)
