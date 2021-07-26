

import math

from .atom import Atom

from utils import Logger


logger = Logger()




class Constant(Atom):
    def __float__(self):
        mapping = {
            "E" : math.e,
            "LOG2E" : math.log2(math.e),
            "LOG10E": math.log10(math.e),
            "LN2" : math.log(2),
            "LN10" : math.log(10),
            "PI" : math.pi,
            "PI_2" : math.pi/2,
            "PI_4" : math.pi/4,
            "M_1_PI" : 1/math.pi,
            "M_2_PI" : 2/math.pi,
            "M_2_SQRTPI" : 2/math.sqrt(math.pi),
            "SQRT2": math.sqrt(2),
            "SQRT1_2" : 1/math.sqrt(2),
            "INFINITY" : math.inf,
        }
        return mapping[self.source]

    def to_wolfram(self):
        mapping = {
            "PI" : "Pi"
        }
        return mapping[self.source]

    def to_sollya(self):
        mapping = {
            "PI" : "pi"
        }
        return mapping[self.source]

    def to_c(self):
        mapping = {
            "PI" : "M_PI"
        }
        return mapping[self.source]




