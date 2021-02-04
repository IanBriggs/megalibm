

from utils.various import parse_float
from utils.logging import Logger


logger = Logger()


# todo: this should probably be arbitrary precision or rationals

class Interval():

    def __init__(self, inf, sup):
        self.inf = parse_float(inf)
        self.sup = parse_float(sup)

        assert(self.inf <= self.sup)


    def __str__(self):
        return "[{},{}]".format(self.inf, self.sup)


    def __repr__(self):
        return "Interval({}, {})".format(self.inf, self.sup)


    def __abs__(self):
        #                 0
        # <---------------+--------------->
        #                    [********]
        if self.inf >= 0.0:
            return Interval(self.inf, self.sup)
        #                 0
        # <---------------+--------------->
        #               [********]
        if self.inf <= 0.0 and 0.0 <= self.sup:
            abs_max = max(-self.inf, self.sup)
            return Interval(0.0, abs_max)
        #                 0
        # <---------------+--------------->
        #      [********]
        if self.sup <= 0.0:
            return Interval(-self.sup, -self.sup)
        else:
            assert 0, "Unreachable"


    def shift(self, k):
        diff = self.sup - self.inf
        shift_by = k*diff
        return Interval(self.inf+shift_by, self.sup+shift_by)


    def split(self, p):
        return self.aligned_split(p, self.inf)


    def aligned_split(self, p, edge):
        assert(0.0 < p)
        assert(self.inf <= edge and edge <= self.sup)

        inf = self.inf
        lower = edge - self.inf
        k = floor(lower/p)
        sup = edge - k*p
        sup = min(sup, self.sup)
        assert(0.0 <= sup-inf and sup-inf <= p)
        if sup-inf != 0:
            periods.append(Interval(inf, sup))

        start = sup
        i=0
        while sup < self.sup:
            inf = start + i*p
            sup = start + (i+1)*p
            sup = min(sup, self.sup)
            assert(self.inf <= inf and sup <= self.sup)
            periods.append(Interval(inf, sup))

        return periods
