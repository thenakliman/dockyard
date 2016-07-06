from pecan import expose, abort, request
from pecan.rest import RestController
from dockyard.engine.common.utils import str_to_dict
from dockyard.engine.common.network.manager import IFManager
from dockyard.engine.controllers.utils import do_not_expose

class InterfaceController(RestController):
    def __init__(self):
        self.network = IFManager()

    @do_not_expose
    @expose()
    def post(self):
        """This method is responsible for creating network interfaces.
        """
        kwargs = str_to_dict(request.body)
        return self.network.create(**kwargs)
       
    @do_not_expose
    @expose()
    def delete(self):
        abort(404)

    @do_not_expose
    @expose()
    def put(self):
        kwargs = str_to_dict(request.body)
        return self.network.update(**kwargs)

    @do_not_expose
    @expose()
    def detach(self):
        abort(404)

     # created this for testing purpose only
    @do_not_expose
    @expose()
    def get_one(self, psid):
        """This method returns networks interfaces in a container.
        """
        psid = int(psid)
        return self.network.get_ifs(psid=psid)

