

import fpcore
import lambdas
from lambdas.lambda_utils import get_mirrors, get_mirrors_at
import lego_blocks
from better_float_cast import better_float_cast
from dirty_equal import dirty_equal
from fpcore.ast import Operation, Variable, Number
from interval import Interval
from lambdas import types
from numeric_types import FP32, FP64
from utils import Logger
import math


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
                 reduction: fpcore.ast.Expr | None,
                 reconstruction: fpcore.ast.Expr | None,
                 synthesize: bool = False,
                 out_type=None):
        self.reduction = reduction
        self.reconstruction = reconstruction
        self.synthesize = synthesize
        super().__init__(in_node)
        self.out_type = out_type

    def __str__(self):
        inner = str(self.in_node)
        if not self.reduction:
            return f"(InflectionLeft <Pending Hole> {self.reconstruction} {inner})"
        return f"(InflectionLeft {self.reduction} {self.reconstruction} {inner})"

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return InflectionLeft(new_in_node, self.reduction, self.reconstruction, synthesize=True)

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

        # TODO: self.synthesize is False from synthesize()
        if self.synthesize:
            lower_domain = Interval(a - (b - a), a)
            if not self.reduction:
                inflextion = better_float_cast(a)
                inf_type = type(better_float_cast)
                str_inf = str(inflextion)
                red_expr = Operation("-",  Number(str(better_float_cast(a))), Variable("x"))
                self.reduction = red_expr
            logger("Evaluating: {}", self.reduction)
            assert type(inner_impl_type) == types.Impl
             # Its an error if the identity is not present
            red_exprs = get_mirrors_at(f, a)
            found_s = False
            for expr in red_exprs:
                if expr == self.reconstruction:
                    found_s = True
                    break
            if not found_s:
                msg = "InflectionLeft requires that '{}' is mirrored about x={}"
                raise TypeError(msg.format(f, a))
            
            self.inflection_point = a
            out_domain = Interval(lower_domain.inf, domain.sup)
            self.out_type = types.Impl(f, out_domain)
            self.type_check_done = True
        else:
            # Using f(x)'s domain [a,b] we need to check that:
            #   for x in [a-(b-a), a] that red(x) is in [a,b]
            lower_domain = Interval(a - (b - a), a)
            if not self.reduction:
                inflextion = better_float_cast(a)
                inf_type = type(better_float_cast)
                str_inf = str(inflextion)
                red_expr = Operation("-",  Number(str(better_float_cast(a))), Variable("x"))
                self.reduction = red_expr
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

            # Set the reduce expression based on the inflection point
            
            
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

        blocks = list()

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
        blocks.append(red)

        blocks.extend(so_far)

        # Reconstruction
        inner_name = self.get_inner_variable(so_far[-1].out_names[0])
        y_out_name = Variable(self.gensym("y_out"))
        self.reconstruction = self.reconstruction.substitute(Variable("x"), Variable("y"))
        rec_expr = self.reconstruction.substitute(
            Variable("y"), inner_name)

        rec = lego_blocks.IfLess(numeric_type,
                                 [x_in_name],
                                 [y_out_name],
                                 better_float_cast(self.inflection_point),
                                 rec_expr.to_libm_c(numeric_type=numeric_type),
                                 inner_name.to_libm_c(numeric_type=numeric_type),
                                 return_type=numeric_type.c_type)
        blocks.append(rec)

        # Out Type
        if self.out_type != None and not self.synthesize:
            cst = lego_blocks.GenerateCast(
                    numeric_type,
                    [y_out_name],
                    [self.gensym("cast_out")],
                    self.out_type.c_type)
            blocks.append(cst)

        return blocks


    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) low high)
        # where (func) is mirrored at point (low+high)/2
        if type(out_type) != types.Impl:
            return list()
        
        # For each mirror point we check to see if our out domain contains it.
        # Then we create the required in domain.
        # This is then used to calculate the actual out domain that would be
        #   made from the in domain.
        # From here er may decide that the mirror point and domain cause too
        #   small an output and so cannot be used, the mirror point is exactly
        #   in the center and required no modification, or the output domain is
        #   too large and requires narrowing.
        # There is a special case for infinite domains since all mirror points
        #   are valid, and infinities can screw up calculations.
        #
        # Eg in this case the mirror point is exactly where it needs to be
        # out domain:      <-----[#############################]----->
        # mirror point:                         |
        # in domain:       <--------------------[##############]----->
        # real out domain: <-----[##############|##############]----->
        #
        # Eg in this case the mirror point is too far to the right to achieve
        #   the full output by mirror
        # out domain:      <-----[#############################]----->
        # mirror point:                              |
        # in domain:       <-------------------------[#########]----->
        # real out domain: <---------------[#########|#########]----->
        #
        # Eg in this case the mirror point means we don't gain anything from
        #   this transformation, so don't generate it
        # out domain:      <-----[#############################]----->
        # mirror point:          |
        # in domain:       <-----[#############################]----->
        # real out domain: <#####|#############################]----->
        #
        # Eg in this case the mirror point pushes the out to be too wide and
        #   require narrowing
        # out domain:      <-----[#############################]----->
        # mirror point:                       |
        # in domain:       <------------------[################]----->
        # real out domain: <-[################|################]----->
        #

        out_domain = out_type.domain
        f = out_type.function
        a = out_domain.inf
        b = out_domain.sup
        mirrors = get_mirrors(f)
        new_holes = list()
        for reconstruction_expr, point in mirrors:
            # reconstruction_expr = reconstruction_expr.substitute(Variable("x"), Variable("y"))
            if (point.contains_op("thefunc") or not point.is_constant()
                or not out_domain.contains(point)
                    or reconstruction_expr.contains_op("thefunc")):
                continue
            in_domain = Interval(point, b)
            in_type = types.Impl(f, in_domain)

            complex = {"sin", "cos", "tan"}
            if any([reconstruction_expr.contains_op(c) for c in complex]):
                continue

            # check for [-inf, inf]
            if (math.isinf(better_float_cast(a))
                and math.copysign(1.0, better_float_cast(a)) == -1.0
                and math.isinf(better_float_cast(b))
                    and math.copysign(1.0, better_float_cast(b)) == 1.0):
                new_holes.append(InflectionLeft(
                    lambdas.Hole(in_type), None, reconstruction_expr, synthesize=True))
                continue

            # check for four cases
            real_out_domain = Interval(in_domain.inf - in_domain.width(),
                                       in_domain.sup)

            # TODO: epsilon comparison
            # match
            if abs(better_float_cast(real_out_domain.inf - a)) < 1e-16:
                new_holes.append(InflectionLeft(
                    lambdas.Hole(in_type), None, reconstruction_expr, synthesize=True))
                continue

            # too small
            if better_float_cast(a) < better_float_cast(real_out_domain.inf):
                continue

            # won't gain anything
            if abs(better_float_cast(in_domain.inf - a)) < 1e-16:
                continue

            # needs narrowing
            new_holes.append(
                lambdas.Narrow(InflectionLeft(lambdas.Hole(in_type), None, reconstruction_expr, synthesize=True),
                       out_domain))

        return new_holes
