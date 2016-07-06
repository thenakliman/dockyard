from pecan import expose, abort, request
from pecan.rest import RestController

from dockyard.engine.common.utils import str_to_dict
from dockyard.engine.common.network.manager import RouteManager
from dockyard.engine.controllers.utils import do_not_expose

class RoutesController(RestController):
    def __init__(self):
        self.routes = RouteManager()

    @do_not_expose
    @expose()
    def delete(self):
        abort(404)

    @do_not_expose
    @expose()
    def post(self):
        kwargs = str_to_dict(request.body)
        return self.routes.routes(**kwargs)

    @do_not_expose
    @expose()
    def get_one(self):
        abort(404)


