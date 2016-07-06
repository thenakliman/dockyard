class URL(object):
    def __init__(self, base_url, dockyard_base_url=None):
        self.base_url = base_url
        if dockyard_base_url:
            self.dockyard_base_url = dockyard_base_url

    def _add_url_id(self, url=None, sub_url=None, id_=None):
        """This method takes base_url and url and ids and combine them
           to make a base url.

           It creates a URL of the format /command/id.
        """
        if not url:
            url = ""

        if id_:
            url = (("%s/%s") % (url, id_))

        if sub_url:
            url =  (("%s/%s") % (url, sub_url))

        return url     

    def make_url(self, url_=None, id_=None):
        """It takes id, url as input and makes complete url, first part
           of url is fetched from object itself.
        """
        url = self._add_url_id(self.base_url, sub_url=url_, id_=id_)
        return url

    def _add_dockyard_url(self, url=None, sub_url=None, id_=None):
        """This method takes base_url and url and ids and combine them
           to make a base url.

           It creates a URL of the format /command/id.
        """
        if not url:
            url = ""

        if sub_url:
            url =  (("%s/%s") % (url, sub_url))

        if id_:
            url = (("%s/%s") % (url, id_))

        return url

 
    def make_dockyard_url(self, url_=None, id_=None):
        """This method makes url for the API specifics to dockyard only.
           This method takes an extra argument of creating dockayrd_base
           which is corresponding to the dockayrd abse URL.
        """
        url = (("%s%s") % (self.dockyard_base_url, self.base_url))
        return self._add_dockyard_url(url=url, sub_url=url_, id_=id_)
