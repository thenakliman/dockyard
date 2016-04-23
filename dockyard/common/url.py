class URL(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def make_url(self, url_=None, id_=None):
        """It takes id, url as input and makes complete url, first part
           of url is fetched from object itself.
        """
        url = self.base_url

        if id_:
            url = (("%s/%s") % (url, id_))

        if url_:
            url =  (("%s/%s") % (url, url_))

        return url
