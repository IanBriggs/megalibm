
from expect import expect_subclass
from fpcore.ast import Variable
from lambdas import types
import lego_blocks
from numeric_types import FP64
import fpcore
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.HIGH)

class Add(types.Transform):

    def __init__(self,
                 num_node: types.Node,
                 den_node: types.Node):
        super().__init__(num_node)
        self.den_node = den_node

    def __str__(self):
        return ("(Add"
                f" {self.in_node} "
                f" {self.den_node})")

    def __repr__(self):
        return ("Add(",
                f"{self.in_node} "
                f"{self.den_node})")

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_num_node = self.in_node.replace_lambda(search, replace)
        new_den_node = self.den_node.replace_lambda(search, replace)
        return Add(new_num_node, new_den_node)

    def type_check(self):
        if self.type_check_done:
            return

        # Make sure the impl we are using can type check
        self.in_node.type_check()
        self.den_node.type_check()

        in_num_function = self.in_node.out_type.function
        in_den_function = self.den_node.out_type.function

        in_num_domain = self.in_node.out_type.domain
        in_den_domain = self.den_node.out_type.domain

        logger.dlog("In numerator: {}", in_num_function)
        logger.dlog("In denominator: {}", in_den_function)

        out_body = in_num_function.body + in_den_function.body

        out_function = fpcore.ast.FPCore("",
                                         in_num_function.arguments,
                                         in_num_function.properties,
                                         out_body)

        logger.dlog("Out function: {}", out_function)

        self.out_type = types.Impl(out_function, in_num_domain)
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        self.type_check()

        num_so_far = super().generate(numeric_type=numeric_type)
        den_so_far = self.den_node.generate(numeric_type=numeric_type)

        x_name = num_so_far[0].in_names[0]
        other_name = den_so_far[0].in_names[0]
        for i in range(len(den_so_far)):
            if den_so_far[i].in_names[0] == other_name:
                den_so_far[i].in_names[0] = x_name

        y_name = self.gensym("add_out")

        add_block = lego_blocks.LegoFPCore(
            numeric_type=numeric_type,
            in_names=[num_so_far[-1].out_names[0], den_so_far[-1].out_names[0]],
            out_names=[y_name],
            fpc=fpcore.parse("(FPCore (a b) (+ a b))")
        )

        return num_so_far + den_so_far + [add_block]