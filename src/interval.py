

import fpcore

from utils.logging import Logger


logger = Logger()


def parse_bound(string):
    wrapped = "(FPCore () {})".format(string)
    fpc = fpcore.parse(wrapped)[0]
    return fpc.body


class Interval():

    def __init__(self, inf, sup):
        self.inf = parse_bound(inf) if type(inf) in {str, float} else inf
        self.sup = parse_bound(sup) if type(sup) in {str, float} else sup

        assert (float(self.inf) <= float(self.sup))

    def __str__(self):
        return "[{},{}]".format(self.inf, self.sup)

    def __repr__(self):
        return 'Interval("{}", "{}")'.format(self.inf, self.sup)

    def __abs__(self):
        #                 0
        # <---------------+--------------->
        #                    [********]
        if float(self.inf) >= 0.0:
            return Interval(self.inf, self.sup)
        #                 0
        # <---------------+--------------->
        #               [********]
        if float(self.inf) <= 0.0 and 0.0 <= float(self.sup):
            abs_max = max(-self.inf, self.sup)
            return Interval(0.0, abs_max)
        #                 0
        # <---------------+--------------->
        #      [********]
        if float(self.sup) <= 0.0:
            return Interval(-self.sup, -self.sup)

        assert 0, "Unreachable"

    def __getitem__(self, items):
        if items == 0:
            return self.inf
        if items == 1:
            return self.sup
        assert False, "TODO: better interval indexing"

    def shift(self, k):
        diff = self.sup - self.inf
        shift_by = k*diff
        return Interval(self.inf+shift_by, self.sup+shift_by)

    def split(self, p):
        return self.aligned_split(p, self.inf)

    def aligned_split(self, p, edge):
        assert (0.0 < p)
        assert (self.inf <= edge and edge <= self.sup)

        inf = self.inf
        lower = edge - self.inf
        k = floor(lower/p)
        sup = edge - k*p
        sup = min(sup, self.sup)
        assert (0.0 <= sup-inf and sup-inf <= p)
        if sup-inf != 0:
            periods.append(Interval(inf, sup))

        start = sup
        i = 0
        while sup < self.sup:
            inf = start + i*p
            sup = start + (i+1)*p
            sup = min(sup, self.sup)
            assert (self.inf <= inf and sup <= self.sup)
            periods.append(Interval(inf, sup))

        return periods
