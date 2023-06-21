

import fpcore
import lego_blocks
from better_float_cast import better_float_cast
from dirty_equal import dirty_equal
from fpcore.ast import Variable
from interval import Interval
from lambdas import types
from numeric_types import FP32, FP64
from utils import Logger

logger = Logger(level=Logger.LOW)

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
        if self.type_check_done:
            return

        # Make sure the impl we are using can type check
        #TODO
        self.in_node.type_check()
        inner_impl_type = self.in_node.out_type
        f = inner_impl_type.function
        domain = inner_impl_type.domain
        a = domain.inf
        b = domain.sup

        # Using f(x)'s domain [a,b] we need to check that:
        #   for x in [a-(b-a), a] that red(x) is in [a,b]
        lower_domain = Interval(a - (b - a), a)
        logger("Evaluating: {}", self.reduction)
        reduced = Interval.try_symbolic_interval_eval(self.reduction,
                                                      lower_domain)
        assert (domain.contains(reduced))

        # We also need to check that:
        #  rec(f(red(x))) == f(x)
        x = Variable("x")
        y = Variable("y")
        rec_f = self.reconstruction.substitute(y, f.body)
        rec_f_red = rec_f.substitute(x, self.reduction)

        # For now let's use a sympy based equality (egg??) ((mpmath???))
        assert (dirty_equal(f, rec_f_red, domain))
        # assert(f.egg_equal(rec_f_red))
        # assert(sympy_based_equal(rec_f_red, f))

        # Set the values that might be used for outer lambda expressions
        self.inflection_point = a
        out_domain = Interval(lower_domain.inf, domain.sup)
        self.out_type = types.Impl(f, out_domain)
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
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
        self.type_check()

        # Generate the inner code first
        so_far = super().generate(numeric_type=numeric_type)

        # Reduction
        x_in_name = Variable(self.gensym("x_in"))
        reduced_name = self.get_inner_variable(so_far[0].in_names[0])
        red_expr = self.reduction.substitute(
            Variable("x"), x_in_name)

        red = lego_blocks.IfLess(numeric_type,
                                 [x_in_name],
                                 [reduced_name],
                                 better_float_cast(self.inflection_point),
                                 red_expr.to_libm_c(numeric_type=numeric_type),
                                 x_in_name.to_libm_c(numeric_type=numeric_type),
                                 return_type=numeric_type.c_type)

        # Reconstruction
        inner_name = self.get_inner_variable(so_far[-1].out_names[0])
        y_out_name = Variable(self.gensym("y_out"))
        rec_expr = self.reconstruction.substitute(
            Variable("y"), inner_name)

        rec = lego_blocks.IfLess(numeric_type,
                                 [x_in_name],
                                 [y_out_name],
                                 better_float_cast(self.inflection_point),
                                 rec_expr.to_libm_c(numeric_type=numeric_type),
                                 inner_name.to_libm_c(numeric_type=numeric_type),
                                 return_type=numeric_type.c_type)

        return [red] + so_far + [rec]
