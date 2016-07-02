# This client will send request to api server, it sends request to API server

from dockyard.engine_client.base import EngineClient
from dockyard.engine_client.container import container
from dockyard.engine_client.image import image
from dockyard.engine_client.network import network
from dockyard.engine_client.volume import volume

class ProcessorRouter(object):
    def __init__(self):
        self.container = container.ContainerRouter()
        self.image = image.Image()
        self.network = network.Network()
        self.volume = volume.Volume()

    def _get_module(self, url):
        modules = url.rsplit(':', 1)[-1].split('/')

        if len(url.rsplit()[-1].split()) == 3:
            module = modules[3]
        else:
            module = modules[2]

        return module

    def _call_operation(self, obj, operation, url, **kwargs):
        try:
            return getattr(obj, "process")(url, operation=operation, **kwargs)
        except AttributeError:
            # Currently no preprocessor or post processor are being done
            # therefor it is passed otherwise InvalidOperation Exception
            # has to be raised
            pass

    def containers(self, url, **kwargs):
        """This method calls appropriate method of the for the
           preprocessing task.
        """
        operation = self._get_module(url)
        return self._call_operation(self.container, operation, url, **kwargs)

    def images(self, url, **kwargs):
        """This method calls appropriate method for pre processing of
           images.
        """
        operation = self._get_module(url)
        return self._call_operation(self.image, operation, url, **kwargs)

    def networks(self, url, **kwargs):
        """This method is responsible for calling method of prepocessing
           of networks.
        """
        operation = self._get_module(url)
        return self._call_operation(self.network, operation, url, **kwargs)

    def volumes(self, url, **kwargs):
        """This method is routes preprocessing tasks to the appropriate
           method of a class for volumes related operations.
        """
        operation = self._get_module(url)
        return self._call_operation(self.volume, operation, url, **kwargs)


class APIServerEngineClient(EngineClient):
    """This method sends request to engine client through api server.
       API server is made to listen for dockyard related CLI. It receives
       request and then perform operation.
    """
    def __init__(self):
        self.router = ProcessorRouter()

    def _get_module(self, url):
        return url.rsplit(':', 1)[-1].split('/')[1]

    def process(self, url, **kwargs):
        module = self._get_module(url)
        return getattr(self.router, module)(url, **kwargs)
