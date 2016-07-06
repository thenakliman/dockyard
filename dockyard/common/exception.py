class DockyardException(Exception):
    def __init__(self, message, **kwargs):
        if message:
            self.message = message
        
        try:
            self.message = self.message % message
        except Exception as e:
            pass

        super(DockyardException, self).__init__(self.message)
            

class IncompleteInfo(DockyardException):
    message = ("%s is missing. Incomplete information.")

class NoValidHostFound(DockyardException):
    message = ("No Valid host for %s is found")
