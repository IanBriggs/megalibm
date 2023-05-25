
from expect import expect_subclass
from fpcore.ast import Variable
from lambdas import types
import lego_blocks
from numeric_types import FP64
import fpcore
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)

class Add(types.Transform):

    def __init__(self,
                 expr: fpcore.ast.Expr,
                 in_node: types.Node):
        super().__init__(in_node)

        # Check and save expr
        expect_subclass("expr", expr, fpcore.ast.Expr)
        self.expr = expr

    def __str__(self):
        return ("(Add"
                f" {self.expr}"
                f" {self.in_node})")

    def __repr__(self):
        return ("Add(",
                f"{self.expr}, "
                f"{self.in_node})")

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return Add(self.expr, self.in_node)

    def type_check(self):
        if self.type_check_done:
            return

        # Make sure the impl we are using can type check
        self.in_node.type_check()

        in_function = self.in_node.out_type.function
        in_domain = self.in_node.out_type.domain

        logger.dlog("In function: {}", in_function)

        out_expr = self.expr + in_function
        out_expr = out_expr.simplify()

        out_function = fpcore.ast.FPCore("",
                                         in_function.arguments,
                                         in_function.properties,
                                         out_expr)

        logger.dlog("Out function: {}", out_function)

        self.out_type = types.Impl(out_function, in_domain)
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        self.type_check()

        so_far = super().generate(numeric_type=numeric_type)

        x = so_far[0].in_names[0]
        p = so_far[-1].out_names[0]

        expr_vars = self.expr.get_variables()
        assert len(expr_vars) == 1
        expr_var = expr_vars.pop()
        poly_var = "p"
        if expr_var == poly_var:
            poly_var = "pp"

        expr = self.expr + Variable(poly_var)
        fpc = fpcore.ast.FPCore(None,
                                [Variable(expr_var), Variable(poly_var)],
                                [],
                                expr)

        sum = lego_blocks.LegoFPCore(numeric_type=numeric_type,
                                     in_names=[x, p],
                                     out_names=[self.gensym("add_out")],
                                     fpc=fpc)
        return so_far + [sum]