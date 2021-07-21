

from .pair import Pair

from utils import Logger


logger = Logger()




class Binding(Pair):
    def __str__(self):
        return "[{} {}]".format(self.name, self.value)
