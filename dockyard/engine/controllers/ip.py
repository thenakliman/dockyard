from pecan import expose, abort, request
from pecan.rest import RestController
from dockyard.engine.common.utils import str_to_dict
from dockyard.engine.common.network.manager import IPManager
from dockyard.engine.controllers.utils import do_not_expose

class IPController(RestController):
    def __init__(self):
        self.ip = IPManager()

    @do_not_expose
    @expose()
    def post(self):
        kwargs = str_to_dict(request.body)
        return self.ip.addr(**kwargs)
 
    @do_not_expose
    @expose()
    def delete(self):
        abort(404)

    @do_not_expose
    @expose()
    def get_one(self, psid=None):
        """This method returns IPs allocated to a container.
        """
        abort(404)


