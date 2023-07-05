

import math
import fpcore
import lambdas
from lambdas.lambda_utils import get_mirrors, get_mirrors_at
import lego_blocks
from better_float_cast import better_float_cast
from dirty_equal import dirty_equal
from fpcore.ast import Number, Operation, Variable
from interval import Interval
from lambdas import types
from numeric_types import FP32, FP64, FPDD
from utils.expr_if_less import ExprIfLess


# This operation takes in an implementation of a function on an interval domain.
# It then produces a new implementation that is valid on a new domain extending
#   past the right edge of the old domain, doubling the width of the domain.
# In addition this operation takes in a reduction and a reconstruction
#   expression.
# For this operation to typecheck the following must be true:
#   given implementation of f(x) valid on domain [a,b]
#   and given the functions red(x) and rec(y)
#   it must be true that:
#     for x in [b, b+(b-a)] that red(x) is in [a,b]
#     and red(f(rec(x))) == f(x)


class InflectionRight(types.Transform):

    def __init__(self,
                 in_node: types.Node,
                 reductions: list[ExprIfLess] | Operation,
                 reconstructions: list[ExprIfLess] | Operation,
                 useDD: bool=False,
                 synthesize: bool=False):
        self.reduction = reductions
        self.reconstruction = reconstructions
        self.useDD = useDD
        self.synthesize = synthesize
        super().__init__(in_node)

    def __str__(self):
        inner = str(self.in_node)
        if not self.reduction:
            return f"(InflectionRight <Pending Hole> {self.reconstruction} {inner})"
        return f"(InflectionRight {self.reduction[0].false_expr} {self.reconstruction[0].false_expr} {inner})"

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return InflectionRight(new_in_node, self.reduction, self.reconstruction, synthesize=True)

    def type_check(self):
        if self.type_check_done:
            return

        # Make sure the impl we are using can type check
        self.in_node.type_check()
        inner_impl_type = self.in_node.out_type
        f = inner_impl_type.function
        domain = inner_impl_type.domain
        a = domain.inf
        b = domain.sup

        if self.synthesize:
            if not self.reduction:
                # TODO: Check
                red_expr = Operation("-",  Number(str(better_float_cast(2 * b))), Variable("x"))
                self.reduction = red_expr

            assert type(inner_impl_type) == types.Impl
             # Its an error if the identity is not present
            red_exprs = get_mirrors_at(f, b)
            found_s = False
            for expr in red_exprs:
                if expr == self.reconstruction:
                    found_s = True
                    break

            if not found_s:
                msg = "InflectionRight requires that '{}' is mirrored about x={}"
                raise TypeError(msg.format(self.function, b))
            self.inflection_point = b
            # TODO: Check
            out_domain = Interval(a, b + (b - a))
            self.out_type = types.Impl(f, out_domain)
            if type(self.reduction) != list:
                assert(type(self.reduction) == Operation)
                red = self.reduction
                ifless_expr = ExprIfLess(None, red)
                self.reduction = [ifless_expr]

            if type(self.reconstruction) != list:
                assert(type(self.reconstruction) == Operation)
                rec = self.reconstruction
                ifless_expr = ExprIfLess(None, rec)
                self.reconstruction = [ifless_expr]
            self.type_check_done = True
        else:
            upper_domain = Interval(b, b + (b- a))

            # If reductions and recunstructions are fpcore convert to list
            if type(self.reduction) != list:
                assert(type(self.reduction) == Operation)
                red = self.reduction
                ifless_expr = ExprIfLess(None, red)
                self.reduction = [ifless_expr]

            if type(self.reconstruction) != list:
                assert(type(self.reconstruction) == Operation)
                rec = self.reconstruction
                ifless_expr = ExprIfLess(None, rec)
                self.reconstruction = [ifless_expr]

            # Using f(x)'s domain [a,b] we need to check that:
            #   for x in [b, b+(b-a)] that red(x) is in [a,b]
            reduced = Interval.try_symbolic_interval_eval(self.reduction[0].false_expr,
                                                        upper_domain)
            assert (domain.contains(reduced))

            # We also need to check that:
            #  rec(f(red(x))) == f(x)
            x = Variable("x")
            y = Variable("y")
            rec_f = self.reconstruction[0].false_expr.substitute(y, f.body)
            rec_f_red = rec_f.substitute(x, self.reduction[0].false_expr)

            # For now let's use a sympy based equality (egg??) ((mpmath???))
            assert (dirty_equal(f, rec_f_red, domain))
            # assert(f.egg_equal(rec_f_red))
            # assert(sympy_based_equal(rec_f_red, f))

            # Set the values that might be used for outer lambda expressions
            self.inflection_point = b
            self.out_type = types.Impl(f, Interval(domain.inf, upper_domain.sup))
            self.type_check_done = True

    def generate(self, numeric_type=FP64):
        # x_in = ...
        # if x_in < inflection_point:
        #   reduced = x_in
        # else:
        #   reduced = reduce(x_in)
        #
        # <inner computation with reduced>
        # inner = ...
        #
        # if x_in < inflection_point:
        #   y_out = inner
        # else:
        #   y_out = reconstruct(y_out)
        self.type_check()

        # Generate the inner code first
        so_far = super().generate(numeric_type=numeric_type)
        
        # Reductions 
        x_in_name = Variable(self.gensym("x_in"))
        red = []
        prevOut = None
        for i, expr_obj in enumerate(self.reduction):
            if i == 0:
                # red_var = self.gensym("gg")
                reduced_name = self.get_inner_variable(so_far[0].in_names[i])
                # SET isDD attrr 
                # reduced_name = reduced_name.setDD(True)
                prevOut = reduced_name
                if numeric_type == FP32:
                    expr_obj.return_type = FP32.c_type
                red_expr = expr_obj.false_expr.substitute(
                Variable("x"), x_in_name)
                red_str = ""
                if self.useDD:
                    red_str =  red_expr.to_libm_c(numeric_type= FPDD) + (".hi" if expr_obj.return_type == "double" else "")
                else:
                    red_str = red_expr.to_libm_c(numeric_type=numeric_type)              

                # Lego blocks need to have Variable("var")/ "var" types so that outer lambda can use it 
                part = lego_blocks.IfLess(numeric_type,
                                        [x_in_name],
                                        [reduced_name],
                                        better_float_cast(self.inflection_point),
                                        x_in_name.to_libm_c(numeric_type=FPDD if expr_obj.compute_type == "dd" else numeric_type),
                                        red_str, 
                                        expr_obj.return_type,
                                        out_cast=True)
                red.append(part)
            else:
                false_expr, true_expr = expr_obj.false_expr, expr_obj.true_expr
                true_var = self.get_inner_variable(prevOut.source + "_hi")
                true_expr = true_expr.substitute(Variable("x"), true_var)
                false_expr = false_expr.substitute(Variable("x"), x_in_name)
                reduced_name = self.get_inner_variable(so_far[0].in_names[i])
                part = lego_blocks.IfLess(numeric_type,
                                          [x_in_name],
                                          [reduced_name],
                                          better_float_cast(self.inflection_point),
                                          true_expr.to_libm_c(numeric_type=numeric_type),
                                          false_expr.to_libm_c(numeric_type=numeric_type),
                                          return_type=expr_obj.return_type)

                red.append(part)

        # Reconstruction
        recons_expr_obj = self.reconstruction[0] 
        in_name = so_far[-1].out_names[0]
        inner_name = self.get_inner_variable(in_name)  
        y_out_name = Variable(self.gensym("y_out"))
        recons_expr_obj.false_expr = recons_expr_obj.false_expr.substitute(Variable("x"), Variable("y"))
        rec_expr = recons_expr_obj.false_expr.substitute(
            Variable("y"), inner_name)

        if numeric_type == FP32:
            recons_expr_obj.return_type = FP32.c_type
        
        recons_str = ""
        if self.useDD:
           recons_str =  rec_expr.to_libm_c(numeric_type= FPDD) + ".hi"
        else:
            recons_str = rec_expr.to_libm_c(numeric_type)

        true_val = inner_name.to_libm_c(numeric_type=FPDD if recons_expr_obj.compute_type == "dd" else numeric_type)
        if recons_expr_obj.compute_type == "dd" and recons_expr_obj.return_type == "double":
            true_val += ".hi"

        rec = lego_blocks.IfLess(numeric_type,
                                 [x_in_name],
                                 [y_out_name],
                                 better_float_cast(self.inflection_point),
                                 true_val,
                                 recons_str, 
                                 return_type=recons_expr_obj.return_type)

        return red + so_far + [rec]

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) low high)
        # where (func) is mirrored at point inside [low, high]
        #   plus extra constraints outlined below
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
        # in domain:       <-----[##############]-------------------->
        # real out domain: <-----[##############|##############]----->
        #
        # Eg in this case the mirror point is too far to the left to achieve
        #   the full output by mirror
        # out domain:      <-----[#############################]----->
        # mirror point:              |
        # in domain:       <-----[###]------------------------------->
        # real out domain: <-----[###|###]--------------------------->
        #
        # Eg in this case the mirror point means we don't gain anything from
        #   this transformation, so don't generate it
        # out domain:      <-----[#############################]----->
        # mirror point:                                        |
        # in domain:       <-----[#############################]----->
        # real out domain: <-----[#############################|#####>
        #
        # Eg in this case the mirror point pushes the out to be too wide and
        #   require narrowing
        # out domain:      <-----[#############################]----->
        # mirror point:                           |
        # in domain:       <-----[################]------------------>
        # real out domain: <-----[################|################]->
        #

        out_domain = out_type.domain
        mirrors = get_mirrors(out_type.function)
        new_holes = list()
        for reconstruction_expr, point in mirrors:
            if (point.contains_op("thefunc") or not point.is_constant()
                or not out_domain.contains(point)
                    or reconstruction_expr.contains_op("thefunc")):
                continue
            in_domain = Interval(out_domain.inf, point)
            in_type = types.Impl(out_type.function, in_domain)

            complex = {"sin", "cos", "tan"}
            if any([reconstruction_expr.contains_op(c) for c in complex]):
                continue

            # check for [-inf, inf]
            if (math.isinf(better_float_cast(out_domain.inf))
                and math.copysign(1.0, better_float_cast(out_domain.inf)) == -1.0
                and math.isinf(better_float_cast(out_domain.sup))
                    and math.copysign(1.0, better_float_cast(out_domain.sup)) == 1.0):
                new_holes.append(InflectionRight(
                    lambdas.Hole(in_type), None, reconstruction_expr, synthesize=True))
                continue

            # check for four cases
            real_out_domain = Interval(in_domain.inf,
                                       in_domain.sup + in_domain.width())

            # TODO: epsilon comparison
            # match
            if abs(better_float_cast(real_out_domain.sup - out_domain.sup)) < 1e-16:
                new_holes.append(InflectionRight(
                    lambdas.Hole(in_type), None, reconstruction_expr, synthesize=True))
                continue

            # too small
            if better_float_cast(real_out_domain.sup) < better_float_cast(out_domain.sup):
                continue

            # won't gain anything
            if abs(better_float_cast(in_domain.sup - out_domain.sup)) < 1e-16:
                continue

            # needs narrowing
            new_holes.append(
                lambdas.Narrow(InflectionRight(lambdas.Hole(in_type), None, reconstruction_expr, synthesize=True), out_domain))

        return new_holes
