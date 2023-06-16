

import fpcore
import lego_blocks
from better_float_cast import better_float_cast
from dirty_equal import dirty_equal
from fpcore.ast import Variable
from interval import Interval
from lambdas import types
from numeric_types import FP32, FP64, FPDD


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

class ExprIfLess:
    def __init__(self, true_expr = None, false_expr = None, return_type = "double", compute="double") -> None:
        self.true_expr = true_expr
        self.false_expr = false_expr
        self.return_type = return_type
        self.compute_type = compute

Exprlist =  list[ExprIfLess]

class InflectionRight(types.Transform):

    def __init__(self,
                 in_node: types.Node,
                 reductions: Exprlist,
                 reconstructions: Exprlist,
                 useDD=False):
        self.reduction = reductions
        self.reconstruction = reconstructions
        self.useDD = useDD
        # self.useDD = False
        super().__init__(in_node)

    def __str__(self):
        inner = str(self.in_node)
        return f"(InflectionRight {self.reduction} {self.reconstruction} {inner})"

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return InflectionRight(new_in_node, self.reduction, self.reconstruction)

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

        # Using f(x)'s domain [a,b] we need to check that:
        #   for x in [b, b+(b-a)] that red(x) is in [a,b]
        upper_domain = Interval(b, b + (b - a))
        # TODO
        # reduced = Interval.try_symbolic_interval_eval(self.reduction[0],
        #                                               upper_domain)
        # assert (domain.contains(reduced))

        # # We also need to check that:
        # #  rec(f(red(x))) == f(x)
        # x = Variable("x")
        # y = Variable("y")
        # rec_f = [recons.substitute(y, f.body) for recons, _ in self.reconstruction]
        # rec_f_red = [rec.substitute(x, self.reduction) for rec in rec_f]

        # # For now let's use a sympy based equality (egg??) ((mpmath???))
        # # TODO
        # assert (dirty_equal(f, rec_f_red[0], domain))
        # assert(f.egg_equal(rec_f_red))
        #assert(sympy_based_equal(rec_f_red, f))

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
        #TODO
        # self.type_check()

        # Generate the inner code first
        so_far = super().generate(numeric_type=numeric_type)

        # Reduction
        # x_in_name = self.gensym("x_in")
        # reduced_name = so_far[0].in_names[0]
        # red_expr = self.reduction.substitute(
        #     Variable("x"), Variable(x_in_name))

        x_in_name = Variable(self.gensym("x_in"))
        red = []
        prevOut = None
        for i, expr_obj in enumerate(self.reduction):
            if i == 0:
                # red_var = self.gensym("gg")
                reduced_name = self.getInnerVariable(so_far[0].in_names[i])
                # SET isDD attrr 
                # reduced_name = reduced_name.setDD(True)
                prevOut = reduced_name
                red_expr = expr_obj.false_expr.substitute(
                Variable("x"), x_in_name)
                red_str = ""
                if self.useDD:
                    red_str =  red_expr.to_libm_c(numeric_type= FPDD) + (".hi" if expr_obj.return_type == "double" else "")
                else:
                    red_str = red_expr.to_libm_c(numeric_type=numeric_type)              

                # part = lego_blocks.IfLess(numeric_type,
                #                         [x_in_name.to_libm_c(numeric_type=FPDD if self.useDD else numeric_type)],
                #                         [reduced_name.to_libm_c(numeric_type=FPDD if self.useDD else numeric_type)],
                #                         better_float_cast(self.inflection_point),
                #                         x_in_name.to_libm_c(numeric_type=FPDD if self.useDD else numeric_type),
                #                         red_str, 
                #                         expr_obj.return_type,
                #                         out_cast=True)
                # Lego blocks need to have Variable("var")/ "var" types so that outer lambda can use it 
                part = lego_blocks.IfLess(numeric_type,
                                        [x_in_name],
                                        [reduced_name],
                                        better_float_cast(self.inflection_point),
                                        x_in_name.to_libm_c(numeric_type=FPDD if expr_obj.compute_type == "dd" else numeric_type),
                                        red_str, 
                                        expr_obj.return_type,
                                        out_cast=True,
                                        compute_type=expr_obj.compute_type)
                red.append(part)
            else:
                false_expr, true_expr = expr_obj.false_expr, expr_obj.true_expr
                true_var = self.getInnerVariable(prevOut.source + "_hi")
                true_expr = true_expr.substitute(Variable("x"), true_var)
                false_expr = false_expr.substitute(Variable("x"), x_in_name)
                reduced_name = self.getInnerVariable(so_far[0].in_names[i])
                # part = lego_blocks.IfLess(numeric_type,
                #                           [x_in_name.to_libm_c(numeric_type=FPDD if self.useDD else numeric_type)],
                #                           [reduced_name.to_libm_c(numeric_type=FPDD if self.useDD else numeric_type)],
                #                           better_float_cast(self.inflection_point),
                #                           true_expr.to_libm_c(numeric_type=numeric_type) + "" if expr_obj.return_type == "double" else ".hi",
                #                           false_expr.to_libm_c(numeric_type=numeric_type))
                part = lego_blocks.IfLess(numeric_type,
                                          [x_in_name],
                                          [reduced_name],
                                          better_float_cast(self.inflection_point),
                                          true_expr.to_libm_c(numeric_type=numeric_type),
                                          false_expr.to_libm_c(numeric_type=numeric_type))

                red.append(part)

        # Reconstruction
        recons_expr_obj = self.reconstruction[0] 
        in_name = so_far[-1].out_names[0]
        inner_name = self.getInnerVariable(in_name)  
        y_out_name = Variable(self.gensym("y_out"))
        rec_expr = recons_expr_obj.false_expr.substitute(
            Variable("y"), inner_name)
        
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
                                 recons_str)

        return red + so_far + [rec]
