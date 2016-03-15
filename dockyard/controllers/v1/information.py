from pecan import expose

class Information(object):
    def __init__(self):
        pass

class Version(object):
    @expose()
    def version(self):
        pass
