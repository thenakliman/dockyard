import abc
import importlib
from oslo_config import cfg
from pecan import request
from urllib3 import PoolManager

ENGINE_CLIENT_OPT = [
    cfg.StrOpt('engine_client',
                default='api_server.api_server.APIServerEngineClient',
                help='Client to be used for sending request to engine')
]

CONF = cfg.CONF
CONF.register_opts(ENGINE_CLIENT_OPT, group='default')

# Fetch scheduler defined in the configuration file and load it.
engine_client_info = CONF.default.engine_client
# May be this path can be specified in the configuration file.
engine_client_loc = 'dockyard.engine_client'
engine_client_info = (('%s.%s') % (engine_client_loc, engine_client_info))
module_name, class_name = engine_client_info.rsplit(".", 1)
engine_client = getattr(importlib.import_module(module_name), class_name)

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
        self.engine_client = engine_client()
        self.pool = PoolManager()

    def _is_local_request(self):
        """This method checks whether this is request for docker engine.
        """
        try:
            request.headers.environ['Request-Status']
        except KeyError:
            status = False
        except:
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
        #req_type = self._is_local_request()
        # Pre processing needs to be done for dockyard feature before
        # performing some actions
        # print method, url, headers, body
        #if req_type: 
        #    self.engine_client.pre_process(method=method, url=url,
        #                                   body=body, headers=headers)
        #else:
        #    headers = self._add_headers(headers)
        headers = {}
        print method, url, headers, body
        data = self.pool.urlopen(method, url, headers=headers, body=body).data
        # Post processing needs to be done for some of the dockyard operations
        #self.engine_client.post_process(method=method, url=url,
        #                               body=body, headers=headers)
        return data
