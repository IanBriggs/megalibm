

from .atom import Atom

from utils import Logger


logger = Logger(level=Logger.EXTRA)




class Number(Atom):
    def __float__(self):
        return float(self.source)

    def to_wolfram(self):
        return self.source

    def to_sollya(self):
        return self.source

    def to_c(self):
        return self.source

