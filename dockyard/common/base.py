import abc
from pecan import request
from urllib3 import PoolManager

class URL(object):
    def __init__(self):
        pass

    @abc.abstractmethod
    def send(self, method, url, headers=None, post_params=None,
                     body=None, **kwargs):
        """This methos is responsible for sending the request.
           :method: Method to be used for sending request.
           :url: URL to be send.
           :headers: headers in the requests.
           :post_params: post parameters.
           :body: Request body.
        """

class DockyardURL(URL):
    def __init__(self):
        self.pool = PoolManager()

    def _is_local_request(self):
        """This method checks whether this is request for docker engine.
        """
        try:
            request.headers.environ['Request-Status']
        except KeyError:
            status = False
        else:
            status = True

        return status

    def send(self, method, url, headers=None, post_params=None,
                     body=None, **kwargs):
        """This methos is responsible for sending the request.
           :method: Method to be used for sending request.
           :url: URL to be send.
           :headers: headers in the requests.
           :post_params: post parameters.
           :body: Request body.
        """
        req_type = self._is_local_request()
        if req_type: 
            preprocess
        else:
            headers = self._add_headers(headers)
        
        data = self.pool.urlopen(method, url, headers=headers, body=body).data
        # post_process
        return data


    def _add_headers(self, headers):
        """This method adds header to each request.
           Valid values for Request-Status header are Scheduled.
           More values will be added, as per requirements.
        """
        if not headers:
            headers = dict()

        headers['Request-Status'] = 'Scheduled'
        return headers
