import os
from better_float_cast import better_float_cast
from fpcore.ast import Variable
import lego_blocks
import numeric_types
# import interval
import lambdas


import snake_egg
import snake_egg_rules

from interval import Interval
from lambdas import types
from snake_egg_rules import operations, egg_to_fpcore
from utils import Logger
import mpmath
from lambdas.lambda_utils import find_periods, has_period
import find_reconstruction


logger = Logger(level=Logger.HIGH)


class PeriodicRecons(types.Transform):

    def __init__(self, in_node: types.Node, period, recons_expr):
        """
        Infinitely expand the domain of an implementation using additive range
          reduction, starting at the left edge of the domain.

        in_node: An implementation valid on a domain with width larger than the
                 period
        period: A period of the function
        """
        self.recons_expr = recons_expr
        self.period = period
        super().__init__(in_node)

    def __str__(self):
        inner = str(self.in_node)
        return f"(PeriodicRecons {self.period} {inner})"

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return PeriodicRecons(new_in_node, period=self.period, recons_expr=self.recons_expr)

    def type_check(self):
        """
        Check that the function has the stated period and the implementation
          has the required width.
        """
        self.in_node.type_check()
        our_in_type = self.in_node.out_type

        float_period = better_float_cast(self.period)

        # TODO: Turn assert into exception
        assert type(our_in_type) == types.Impl
        # TODO: Type check on periods
        assert has_period(our_in_type.function, float_period)
        assert better_float_cast(our_in_type.domain.width()) <= float_period

        self.domain = Interval("(- INFINITY)", "INFINITY")
        self.out_type = types.Impl(our_in_type.function,
                                   self.domain)

    def generate(self):
        # in = ...
        # k = floor((in-sup) / period)
        # out = in - period * k
        # ...
        so_far = super().generate()
        in_name = self.gensym("in")
        out_name = so_far[0].in_names[0]

        k = self.gensym("k")
        add = lego_blocks.SimpleAdditive(numeric_types.fp64(), [in_name],
                                         [out_name, k], self.in_node.domain.inf, self.period)

        # Inductive reconstruction to map the output according to its s function | (s(f(t(x))))
        inner_name = so_far[-1].out_names[0]
        recons_name = self.gensym("recons")
        ind_recons = lego_blocks.Expression(numeric_types.fp64(),
                                         [inner_name, k],
                                         [recons_name],
                                         self.recons_expr)

        return [add] + so_far + [ind_recons]

    @classmethod
    def is_valid_expr(cls, expr):
        return expr != operations.recons("k")

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
        new_holes = list()
        for s, p in periods:
            # We only care about s which are not handled by Periodic lambda
            if p.contains_op("thefunc") or better_float_cast(p) == 0.0 or s.contains_op("thefunc") or s == Variable("x"):
                continue
            # Use e-graph intersection to find the s reconstruction and check if its valid
            extracted = find_reconstruction.get_reconstruction(s)
            if not cls.is_valid_expr(extracted):
                continue
            recons_expr = egg_to_fpcore(extracted)
            if better_float_cast(p) < 0.0:
                p = -p
            pos = types.Impl(out_type.function, Interval(0.0, p))
            new_holes.append(PeriodicRecons(
                lambdas.Hole(pos), p, recons_expr))
            cen = types.Impl(out_type.function, Interval(-p / 2, p / 2))
            new_holes.append(PeriodicRecons(
                lambdas.Hole(cen), p, recons_expr))

        return new_holes
