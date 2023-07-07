
import cmd_sollya
from expect import expect_subclass
from fpcore.ast import Variable
from interval import Interval
from lambdas import types
import lego_blocks
from numeric_types import FP64
import fpcore
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)

class ApproxError(Exception):
    def __init__(self, outer_func, inner_func, domain, epsilon, actual):
        self.outer_func = outer_func
        self.inner_func = inner_func
        self.domain = domain
        self.epsilon = epsilon
        self.actual = actual

    def __str__(self):
        return "\n".join([f"Outer func: {self.outer_func}",
                          f"Inner func: {self.inner_func}",
                          f"Domain: {self.domain}"
                          f"Epsilon: {self.epsilon}",
                          f"InfNorm: {self.actual}"])

class Approx(types.Transform):

    def __init__(self,
                 new_function: fpcore.ast.FPCore,
                 new_domain: Interval,
                 epsilon: float,
                 in_node: types.Node):
        super().__init__(in_node)
        self.new_function = new_function
        self.new_domain = new_domain
        self.epsilon = epsilon

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return Approx(self.new_function, self.new_domain, self.epsilon, new_in_node)

    def type_check(self):
        if self.type_check_done:
            return

        # Make sure the impl we are using can type check
        self.in_node.type_check()

        in_function = self.in_node.out_type.function
        din = cmd_sollya.DirtyInfNorm(in_function.body,
                                      self.new_function,
                                      self.new_domain)

        if din > self.epsilon:
            raise ApproxError(self.new_function, in_function,
                              self.new_domain,
                              self.epsilon, din)

        self.out_type = types.Impl(self.new_function, self.new_domain)
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        self.type_check()

        so_far = super().generate(numeric_type=numeric_type)

        return so_far