import abc


class Membership(object):
    @abc.abstractmethod
    def get_all_host(self):
        """This method returns all the hosts available in the 
           data center.
        """
