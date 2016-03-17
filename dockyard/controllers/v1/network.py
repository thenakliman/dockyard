from pecan import expose

class Network(object):
    def __init__(self):
        return
    
class NetworkController(object):
    def __init__(self):
        pass

    @expose(generic=True)
    def index(self, *name_or_id, **kwargs):
        return "Get name of the networks:"

    @index.when(method='POST')
    def set_network(self, _id, *connect):
        return "Set network"

    @expose(generic=True)
    def create(self):
        return "Invalid"

    @create.when(method="POST")
    def create(self, *args):
        return "create"
