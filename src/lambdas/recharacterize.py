
import mpmath
import sympy

import lego_blocks
from dirty_equal import dirty_equal
from interval import Interval
from lambdas import types
from numeric_types import FP64
from sympy_solve_equality import sympy_solve_equality, sympy_to_fpcore
from utils import Logger

logger = Logger(level=Logger.LOW)  # HIGH)


class Recharacterize(types.Transform):

    def __init__(self,
                 out_function,
                 remapping_function,
                 in_node):
        super().__init__(in_node)
        self.out_function = out_function
        self.remapping_function = remapping_function

    def __str__(self):
        return ("(Recharacterize"
                f" {self.out_function}"
                f" {self.remapping_function}"
                f" {self.in_node})")

    def rewrite_to_use_var(self, expr, var):
        vars = expr.get_variables()
        if vars == {var.source}:
            return expr

        # See if we can remove an extra variable using the remapping
        in_var = self.in_node.out_type.function.arguments[0]
        remap = self.remapping_function.body
        if var != in_var and in_var.source in vars:
            expr = expr.substitute(in_var, remap)

        # See if the inverse mapping can be used
        out_var = self.out_function.arguments[0]
        if var != out_var and out_var.source in vars:
            inverse_map = sympy_solve_equality(in_var, remap, out_var)
            expr = expr.substitute(out_var, inverse_map)
            pass

        # Did this reach the goal?
        vars = expr.get_variables()
        if vars == {var.source}:
            return expr

        # Try up a level if possible
        if self.parent is None:
            msg = (f"Unable to rewrite expression to just use `{var}`:\n"
                   f" expr: '{expr}'")
            raise ValueError(msg)
        return self.parent.rewrite_to_use_var(expr, var)

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return Recharacterize(self.out_function,
                              self.remapping_function,
                              self.in_node)

    def type_check(self):
        if self.type_check_done:
            return

        # Make sure the impl we are using can type check
        self.in_node.type_check()

        # Each function will have it's own variable name, so we need to keep
        # this straight.
        # Make sure that the input and output functions have different variable
        # names, and that the remapping function uses the input function's
        # variable
        in_function = self.in_node.out_type.function
        in_var = in_function.arguments[0]
        out_var = self.out_function.arguments[0]
        rem_var = self.remapping_function.arguments[0]

        if in_var == out_var:
            msg = ("Recharacterize must be called with an output function that"
                   " uses a different variable than the input."
                   f" Both were: '{in_var}'")
            raise ValueError(msg)

        if rem_var != out_var:
            msg = ("Recharacterize must be called with a remapping function"
                   " using the variable of the output function")
            raise ValueError(msg)

        # We need to figure out what the new domain will be
        # Using the standard log1p mapping as an example:
        #   in = log(1+z)
        #   out = log(x)
        #   rem = x - 1
        # Where the domain of `in` is [0, 1]
        # This means we need to solve z = x - 1 for x
        #   z = x - 1
        #   z + 1 = x
        # Then we can use interval arithmetic to determine the domain of x
        #   [0, 1] + 1 = x
        #   [1, 2] = x
        in_domain = self.in_node.out_type.domain
        logger("{} has domain of [{}, {}]",
               in_var,
               in_domain.float_inf,
               in_domain.float_sup)
        remap = self.remapping_function.body
        inverse_map = sympy_solve_equality(in_var, remap, out_var)
        logger("Inverse of {} is {}", remap, inverse_map)

        out_domain = Interval.try_symbolic_interval_eval(
            inverse_map, in_domain)
        logger("{} has domain of [{}, {}]",
               out_var,
               out_domain.float_inf,
               out_domain.float_sup)

        # We need to make sure the two functions are equivalent in this domain.
        in_function_wrt_out_var = in_function.substitute(in_var, remap)

        if not dirty_equal(self.out_function,
                           in_function_wrt_out_var,
                           out_domain):
            msg = ("Unable to test equal:\n"
                   f"  in: {in_function}\n"
                   f"  out: {self.out_function}\n"
                   f"  var: {self.remapping_function}")
            raise ValueError(msg)

        self.out_type = types.Impl(self.out_function, out_domain)
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        # x = ...
        # z = remap(x)
        # ...
        self.type_check()

        # Generate the inner code first
        so_far = super().generate(numeric_type=numeric_type)

        x = self.gensym("recharacterize_in")
        z = so_far[0].in_names[0]

        remapping = lego_blocks.LegoFPCore(numeric_type,
                                           [x],
                                           [z],
                                           self.remapping_function)

        # See if any inner blocks use the recharacterize name
        out_var = self.out_function.arguments[0]
        for i, b in enumerate(so_far):
            for j, n in enumerate(b.in_names):
                if type(n) == types.VariableRequest and n.var == out_var:
                    so_far[i].in_names[j] = x

        return [remapping] + so_far
