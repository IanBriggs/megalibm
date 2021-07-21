

from .pair import Pair

from utils import Logger


logger = Logger()




class Property(Pair):
    def __str__(self):
        value_str = str(self.value)
        if type(self.value) in {tuple, list}:
            value_str = "({})".format(list_to_str(self.value))
        return ":{} {}".format(self.name, value_str)
