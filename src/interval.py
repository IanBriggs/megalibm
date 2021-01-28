

from utils.various import parse_float
from utils.logging import Logger


logger = Logger()




class Interval():

    def __init__(self. inf, sup):
        self.inf = parse_float(inf)
        self.sup = parse_float(sup)

        assert(self.inf <= self.sup)


    def __str__(self):
        return "[{},{}]".format(self.inf, self.sup)


    def __repr__(self):
        return "Interval({}, {})".format(self.inf, self.sup)


    def __abs__(self):
        if self.inf >= 0.0:
            return Interval(self.inf, self.sup)
        if self.inf <= 0.0 and 0.0 <= self.sup:
            abs_max = max(-self.inf, self.sup)
            return Interval(0.0, abs_max)
        if self.sup <= 0.0:
            return Interval(-self.sup, -self.sup)
        else:
            assert 0, "Unreachable"
