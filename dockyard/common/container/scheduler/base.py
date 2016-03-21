import abc


class Scheduler(object):
    @abc.abstractmethod
    def get_host(self, *args, **kwargs):
        """This method returns host information to launch
           container.

           It expects specification of docker container and 
           interact with membership managment protocol to
           find the host to run a container.

           Every scheduler should have this method.
        """
