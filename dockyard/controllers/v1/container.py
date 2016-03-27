from pecan import expose, abort

from dockyard.common.container import container 
class Container(object):
    def __init__(self):
        self.container = container.Container()

    @expose(generic=True)
    def index(self):
       return "index"	

    @expose()
    def json(self, name_id=None):
        return self.container.list(name_id)

    @expose()
    def stats(self, _id):
        return self.container.stats(_id)

    @expose(generic=True)
    def archive(self, _id):
        return self.container.archive(_id)

    @archive.when(method="PUT")
    def upload(self, _id):
        return self.container.upload(_id)

    @expose(generic=True)
    def copy(self, _id):
        abort(404)

    @copy.when(method="POST")
    def copy_POST(self, _id):
        return self.container.copy(_id)

    @expose(generic=True)
    def logs(self, _id):
        return self.container.logs(_id)
    	
    @expose(generic=True)
    def start(self):
        abort(404)

    @start.when(method="POST")
    def start_POST(self,  _id):
        return self.container.start(_id)

    @expose(generic=True, route='exec')
    def exe(self):
        abort(404)

    @exe.when(method="POST")
    def exec_POST(self, _id):
        return self.container.exe(_id) 

    @expose(generic=True)
    def attach(self):
        abort(404)

    @attach.when(method="POST")
    def attach_POST(self, _id):
        return self.container.attach(_id)

    @expose(generic=True)
    def rename(self):
        abort(404)

    @rename.when(method="POST")
    def rename_POST(self, _id):
        return self.container.rename(_id)


class ContainerController(object):
    def __init__(self):
        pass

#    @expose(generic=True)
#    def create(self, *args):
#        abort(404)

#    @create.when(method="POST")
#    def create_container(self, *args):
#        return self.container.create(args)

    @expose()
    def json(self):
        return Container().json()

    @expose()
    def _lookup(self, id_name_op=None, op=None):
        new_url = []
        print("Inside ++++++++++")
        if op:
            new_url.append(op)
        elif id_name_op:
            new_url.append(id_name_op)

        if op:
            new_url.append(id_name_op)

        if new_url:        
           new_url = tuple(new_url)
        else:
           new_url = tuple([''])  

        print(new_url)
        return Container(), new_url
