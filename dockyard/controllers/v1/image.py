from pecan import expose, route

class Image(object):
    def __init__(self):
        pass
   
    @expose() 
    def push(self, _id):
        return "PUSH %d Image"

    @expose(generic=True)
    def create(self, *args):
        return "Invalid Create"

    @create.when(method="POST")
    def create_POST(self, *args):
        return "Valid create"

    @expose()
    def json(self, _id=None):
        return "details"     

class ImageController(object):
    def __init__(self):
        pass

    @expose()
    def _lookup(self, _id, op):
        return Image(), (op + _id);
route('json', Image().json)
