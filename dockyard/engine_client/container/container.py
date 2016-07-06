from dockyard.engine_client.container.pre_container import PreProcessor
from dockyard.engine_client.container.post_container import PostProcessor

class ContainerRouter(object):
    """This class takes care of post processing and pre processing
       required for providing the functionality of dockyard.
    """
    mapping = {
                   "pre": "pre_processor",
                   "post": "post_processor"
              }

    def __init__(self):
        self.pre_processor = PreProcessor()
        self.post_processor = PostProcessor()

    def _call_operation(self, url, **kwargs):
        try:
            obj = getattr(self, ContainerRouter.mapping[kwargs["r_type"]])
            return getattr(obj, kwargs["operation"])(url, **kwargs)
        except AttributeError:
            # Currently no preprocessor or post processor are being done
            # therefor it is passed otherwise InvalidOperation Exception
            # has to be raised
            pass

    def process(self, url, **kwargs):
        """This method routes the request to appropriate method of the class
           depending on the whether it is pre processing request or post
           processing request.
        """
        self._call_operation(url=url, **kwargs)
