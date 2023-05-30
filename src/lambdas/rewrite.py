
from dirty_equal import dirty_equal
from expect import expect_subclass
from fpcore.ast import Variable
from lambdas import types
import lambdas
import lego_blocks
from numeric_types import FP64
import fpcore
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)

class Rewrite(types.Transform):

    def __init__(self,
                 from_expr: fpcore.ast.Expr,
                 to_expr: fpcore.ast.Expr,
                 in_node: types.Node):
        super().__init__(in_node)

        expect_subclass("from_expr", from_expr, fpcore.ast.Expr)
        self.from_expr = from_expr

        expect_subclass("to_expr", to_expr, fpcore.ast.Expr)
        self.to_expr = to_expr

    def __str__(self):
        return ("(Rewrite"
                f" {self.from_expr}"
                f" {self.to_expr}"
                f" {self.in_node})")

    def __repr__(self):
        return ("Rewrite(",
                f"{self.expr}, "
                f"{self.to_expr}, "
                f"{self.in_node})")

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return Rewrite(self.expr, self.in_node)

    def type_check(self):
        if self.type_check_done:
            return

        # Make sure the impl we are using can type check
        self.in_node.type_check()
        in_function = self.in_node.out_type.function
        in_domain = self.in_node.out_type.domain

        # TODO: Hacked to only work with an `Add` inside
        assert type(self.in_node) == lambdas.Add

        # Make sure the rewrite is valid
        # To do this first rewrite both expressions using known equalities
        # until they are both in terms of the `in_functions`'s input variable
        in_var = in_function.arguments[0]

        # These calls require that we have already set our out_type
        self.out_type = types.Impl(in_function, in_domain)
        from_expr = self.parent.rewrite_to_use_var(self.from_expr, in_var)
        to_expr = self.parent.rewrite_to_use_var(self.to_expr, in_var)

        # Make sure they are equal
        if not dirty_equal(from_expr, to_expr, in_domain):
            msg = ("Invalid rewrite, given expressions are not equal:\n"
                   f" from: '{self.from_expr}'\n"
                   f"   to: '{self.to_expr}'")
            raise ValueError(msg)

        # Make sure the `from_expr` is present
        if not self.in_node.expr.contains(self.from_expr):
            msg = ("Invalid rewrite, given `from_expr` not found:\n"
                   f" from_expr: '{self.from_expr}'"
                   f"      expr: '{self.in_node.expr}'")
            raise ValueError(msg)

        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        self.type_check()

        # Change the `Add`
        old = self.in_node.expr
        self.in_node.expr = old.substitute(self.from_expr, self.to_expr)

        so_far = super().generate(numeric_type=numeric_type)

        # Undo change incase the inner lambda is used elsewhere
        self.in_node.expr = old

        return so_far