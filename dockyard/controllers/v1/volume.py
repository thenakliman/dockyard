class VolumeController(object):
    def __init__(self):
        pass

    @expose(generic=True)
    def index(self, name=None):
        return "index"

    @index.when(method='DELETE')
    def index_delete(self, name)
        return "Delete Volume"
   
    @expose(generic=True)
    def create(self):
        return "create"

    @create.when(method='POST')
    def create(self):
        return "create"
