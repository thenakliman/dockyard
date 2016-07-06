from pecan import expose

def do_not_expose(method):
    def dont_expose(self, *args, **kwargs):
        return self.method(*args, **kwargs)
    return dont_expose
