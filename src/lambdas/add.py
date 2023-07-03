
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
                 in_node: types.Node,
                 useDD=False):
        super().__init__(in_node)

        # Check and save expr
        expect_subclass("expr", expr, fpcore.ast.Expr)
        self.expr = expr
        self.useDD = useDD

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

        expr_vars = self.expr.get_variables()
        fpcore_arguments = list()
        lego_arguments = list()

        # TODO: Currently hoping the name "p" doesn't clash
        assert "p" not in expr_vars
        p_var = fpcore.ast.Variable("p")
        fpcore_arguments.append(p_var)
        lego_arguments.append(so_far[-1].out_names[0])

        x_var = self.out_type.function.arguments[0]
        if x_var.source in expr_vars:
            fpcore_arguments.append(x_var)
            lego_arguments.append(so_far[0].in_names[0])
            expr_vars.remove(x_var.source)

        for fpcore_var_str in expr_vars:
            var = fpcore.ast.Variable(fpcore_var_str)
            fpcore_arguments.append(var)
            lego_arguments.append(types.VariableRequest(var))

        these_blocks = list()

        if self.useDD:
            e = fpcore.ast.FPCore(None, fpcore_arguments, [], self.expr)
            ename = self.gensym("add_intermediate")
            eblock = lego_blocks.LegoFPCore(numeric_type=numeric_type,
                                            in_names=lego_arguments,
                                            out_names=[ename],
                                            fpc=e)
            these_blocks.append(eblock)
            sum = lego_blocks.AssignDD(in_names = [ename, so_far[-1].out_names[0]],
                                       out_names = [self.gensym("add_out")])
            these_blocks.append(sum)
        else:
            expr = self.expr + p_var
            fpc = fpcore.ast.FPCore(None,
                                    fpcore_arguments,
                                    [],
                                    expr)

            sum = lego_blocks.LegoFPCore(numeric_type=numeric_type,
                                         in_names=lego_arguments,
                                         out_names=[self.gensym("add_out")],
                                         fpc=fpc)
            these_blocks.append(sum)
        return so_far + these_blocks