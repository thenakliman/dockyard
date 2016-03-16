from pecan import expose

class Information(object):
    def __init__(self):
        pass
   
    @expose()
    def index(self):
        return "Info"

class Version(object):
    @expose()
    def index(self):
        return "version" 
