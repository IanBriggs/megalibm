
import lambdas
import lego_blocks
from better_float_cast import better_float_cast
from fpcore.ast import Variable
from interval import Interval
from lambdas import types
from lambdas.lambda_utils import find_periods, has_period
from numeric_types import fp64
from utils import Logger

logger = Logger(level=Logger.HIGH)


class Periodic(types.Transform):

    def __init__(self, in_node: types.Node, period):
        """
        Infinitely expand the domain of an implementation using additive range
          reduction, starting at the left edge of the domain.

        in_node: An implementation valid on a domain with width larger than the
                 period
        period: A period of the function
        """
        self.period = period
        super().__init__(in_node)

    def __str__(self):
        inner = str(self.in_node)
        return f"(periodic {self.period} {inner})"

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return Periodic(new_in_node, period=self.period)

    def type_check(self):
        """
        Check that the function has the stated period and the implementation
          has the required width.
        """
        if self.type_check_done:
            return

        self.in_node.type_check()
        our_in_type = self.in_node.out_type

        float_period = better_float_cast(self.period)

        #TODO: Turn assert into exception
        assert type(our_in_type) == types.Impl
        assert has_period(our_in_type.function, float_period)
        assert better_float_cast(our_in_type.domain.width()) <= float_period

        self.domain = Interval("(- INFINITY)", "INFINITY")
        self.out_type = types.Impl(our_in_type.function,
                                   self.domain)
        self.type_check_done = True

    def generate(self, numeric_type=fp64):
        # in = ...
        # k = floor((in-sup) / period)
        # out = in - period * k
        # ...
        self.type_check()

        so_far = super().generate(numeric_type=numeric_type)
        in_name = self.gensym("in")
        out_name = so_far[0].in_names[0]

        k = self.gensym("k")
        add = lego_blocks.SimpleAdditive(numeric_type(),
                                         [in_name],
                                         [out_name, k],
                                         self.in_node.domain.inf,
                                         self.period)

        return [add] + so_far

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) -INFINITY INFINITY)
        # where (func) is periodic
        if (type(out_type) != types.Impl
            or better_float_cast(out_type.domain.inf) != -better_float_cast("inf")
                or better_float_cast(out_type.domain.sup) != better_float_cast("inf")):
            return list()

        # To get this output we need as input
        # (Impl (func) low high)
        # where high-low is less than or equal to a period of func

        # Get periods and try both [0, period] and [-period/2, period/2]
        periods = find_periods(out_type.function)
        periods = [t_arg for s, t_arg in periods if s == Variable("x") and not t_arg.contains_op("thefunc")]
        periods.sort(key=float, reverse=True)
        floats = set()
        new_holes = list()
        for p in periods:
            fp = better_float_cast(p)
            if fp < 0:
                fp = -fp
                p = -p
            if fp == 0.0 or fp in floats:
                continue
            pos = types.Impl(out_type.function, Interval(0.0, p))
            new_holes.append(Periodic(lambdas.Hole(pos), p))
            cen = types.Impl(out_type.function, Interval(-p/2, p/2))
            new_holes.append(Periodic(lambdas.Hole(cen), p))
            floats.add(fp)

        return new_holes
