import abc
import random
import string

class Random(object):
    def __init__(self):
        assert(False)

    @abc.abstractmethod 
    def get_number(self, length):
        """This number generate a random string from of given
           length.
        """

class RandomNumber(Random):
    """This class generate random string.
    """
    def __init__(self):
        pass

    def get_number(self, length):
        """This method returns a random string of length.
           random strings can be in lower case, upper case
           and digits.
        """
        choices = (string.ascii_lowercase + string.ascii_uppercase +
                   string.digits)

        rand = (''.join(random.SystemRandom().choice(choices)
                for _ in range(length)))

        return rand
