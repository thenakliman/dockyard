from oslo_config import cfg
from pecan import expose, abort, rest


# Fetch scheduler defined in the configuration file and load it.
network_driver_info = CONF.default.network_driver
# May be this path can be specified in the configuration file.
network_driver_loc = 'engine.common.network.drivers'
network_driver_info = (('%s.%s') % (nework_driver_loc, network_driver_info))
module_name, class_name = scheduler_info.rsplit(".", 1)
class_ = getattr(importlib.import_module(module_name), class_name)
network = class_()


class Interface(rest.Controller):
    def __init__(self):
        pass

    @expose()
    def post(self):
        pass
       
    @expose()
    def delete(self):
        pass

    @expose()
    def attach(self):
        pass

    @expose()
    def move(self):
        pass

    @expose()
    def detach(self):
        pass

    @expose()
    def get_all(self):
        pass

    @expose()
    def get_one(self):
        pass

class Routes(rest.Controller):
    def __init__(self):
        pass

    @expose()
    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

    def get_one(self):
        pass


class IP(rest.Controller)
    def __init__(self):
        pass

    @expose()
    def put(self):
        pass
 
    @expose()
    def delete(self):
        pass

    @expose()
    def udpate(self):
        pass

    @expose()
    def get_one(self):
        pass
