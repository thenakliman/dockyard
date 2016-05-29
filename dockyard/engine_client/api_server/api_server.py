# This client will send request to api server, it sends request to API server

from dockyard.engine_client.clients.base import EngineClient
from dockyard.engine_client.clients.containers import PreProcessor
from dockyard.engine_client.clients.containers import PostProcessor


class APIServerEngineClient(EngineClient):
    """This method sends request to engine client through api server.
       API server is made to listen for dockyard related CLI. It receives
       request and then perform operation.
    """
    def __init__(self):
        self.pre_process = PreProcessor()
        self.post_process = PostProcessor()

    def _get_module(self, url):
        return url.rsplit(':', 1)[-1].split('/')[1]

    def pre_process(self, url, **kwargs):
        module = self._get_module(url, **kwargs)
        return getattr(self.pre_process, module)(url, **kwargs)
        

    def post_process(self, url, **kwargs):
        module = self._get_module(url, **kwargs)
        return getattr(self.post_process, module)(url, **kwargs)
