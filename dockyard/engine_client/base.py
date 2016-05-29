# This module acts as a base class for the other clients. All the clients must
# inherit this class
import abc

class EngineClient(object):
    def __init__(self):
        pass

    @abc.abstractmethod
    def pre_process(self, **kwargs):
        """This method is responsible for sending requests related to dockyard
           before launching container.
        """

    @abc.abstractmethod
    def post_process(self, **kwargs):
        """This method is reponsible for sending request related to dockyard
           after container has been created.
        """
        pass
