
import math
from better_float_cast import better_float_cast
from fpcore.ast import Variable
from lambdas.narrow import Narrow
import lego_blocks
from numeric_types import fp64, fp32
import lambdas

import fpcore

from dirty_equal import dirty_equal

from interval import Interval
from lambdas import types
from sympy_based_equal import sympy_based_equal
from utils import Logger

# This operation takes in an implementation of a function on an interval domain.
# It then produces a new implementation that is valid on a new domain extending
#   past the left edge of the old domain, doubling the width of the domain.
# In addition this operation takes in a reduction and a reconstruction
#   expression.
# For this operation to typecheck the following must be true:
#   given implementation of f(x) valid on domain [a,b]
#   and given the functions red(x) and rec(y)
#   it must be true that:
#     for x in [a-(b-a), a] that red(x) is in [a,b]
#     and red(f(rec(x))) == f(x)


class InflectionLeft(types.Transform):

    def __init__(self,
                 in_node: types.Node,
                 reduction: fpcore.ast.Expr,
                 reconstruction: fpcore.ast.Expr):
        self.reduction = reduction
        self.reconstruction = reconstruction
        super().__init__(in_node)

    def __str__(self):
        inner = str(self.in_node)
        return f"(InflectionLeft {self.reduction} {self.reconstruction} {inner})"

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return InflectionLeft(new_in_node, self.reduction, self.reconstruction)

    def type_check(self):
        # Make sure the impl we are using can type check
        self.in_node.type_check()
        inner_impl_type = self.in_node.out_type
        f = inner_impl_type.function
        domain = inner_impl_type.domain
        a = domain.inf
        b = domain.sup

        # Using f(x)'s domain [a,b] we need to check that:
        #   for x in [a-(b-a), a] that red(x) is in [a,b]
        lower_domain = Interval(a-(b-a), a)
        reduced = self.reduction.interval_eval({"x": lower_domain})
        assert(domain.contains(reduced))

        # We also need to check that:
        #  rec(f(red(x))) == f(x)
        x = Variable("x")
        y = Variable("y")
        rec_f = self.reconstruction.substitute(y, f.body)
        rec_f_red = rec_f.substitute(x, self.reduction)

        # For now let's use a sympy based equality (egg??) ((mpmath???))
        assert(dirty_equal(f, rec_f_red, domain))
        #assert(f.egg_equal(rec_f_red))
        #assert(sympy_based_equal(rec_f_red, f))

        # Set the values that might be used for outer lambda expressions
        self.inflection_point = a
        self.domain = Interval(a-(b-a), b)
        self.passed_check = True
        self.out_type = types.Impl(f, self.domain)


    def generate(self, numeric_type=fp64):
        # x_in = ...
        # if x_in < inflection_point:
        #   reduced = reduce(x_in)
        # else:
        #   reduced = x_in
        #
        # <inner computation with reduced>
        # inner = ...
        #
        # if x_in < inflection_point:
        #   y_out = reconstruct(y_out)
        # else:
        #   y_out = inner

        # Generate the inner code first
        so_far = super().generate(numeric_type=numeric_type)

        # Reduction
        x_in_name = self.gensym("x_in")
        reduced_name = so_far[0].in_names[0]
        red_expr = self.reduction.substitute(Variable("x"), Variable(x_in_name))
        if isinstance(numeric_type(), fp32):
            red_expr = red_expr.substitute_op()

        red = lego_blocks.IfLess(numeric_type(),
                               [x_in_name],
                               [reduced_name],
                               better_float_cast(self.inflection_point),
                               red_expr.to_libm_c(numeric_type=numeric_type()),
                               x_in_name)

        # Reconstruction
        inner_name = so_far[-1].out_names[0]
        y_out_name = self.gensym("y_out")
        rec_expr = self.reconstruction.substitute(Variable("y"), Variable(inner_name))
        if isinstance(numeric_type(), fp32):
            rec_expr = rec_expr.substitute_op()

        rec = lego_blocks.IfLess(numeric_type(),
                                       [x_in_name],
                                       [y_out_name],
                                       better_float_cast(self.inflection_point),
                                       rec_expr.to_libm_c(numeric_type=numeric_type()),
                                       inner_name)

        return [red] + so_far + [rec]

