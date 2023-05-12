

from math import sqrt
import find_reconstruction
import fpcore
import lambdas
import lego_blocks
from better_float_cast import better_float_cast
from fpcore.ast import Variable
from interval import Interval
from lambdas import types
from lambdas.lambda_utils import find_periods, has_period
from numeric_types import FP64
from snake_egg_rules import egg_to_fpcore, operations
from utils import Logger

logger = Logger(level=Logger.HIGH)


class Multiplicative(types.Transform):
    """
    Reduce input x into integer k and float m such that x = m * 2**k
    and m is in a defined reduced range.
    Reconstruct f(x) as f(m) + k*f(2)
    """

    def __init__(self,
                 in_node: types.Node):
        super().__init__(in_node)

    def __str__(self):
        inner = str(self.in_node)
        return f"(Multiplicative {inner})"

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return Multiplicative(new_in_node)

    def type_check(self):
        if self.type_check_done:
            return

        self.in_node.type_check()
        our_in_type = self.in_node.out_type

        # TODO: Check that f(x) == f(x/2) + f(2)

        # TODO: Check that the domain of the inner impl will work
        # FP decomposition gives an `m` on [1.0, 2.0)
        # The inner impl needs to work with this, but I'm not sure how
        # to determine "works with".
        # For instance, the smaller domain [0.5, 1.0) is fine and just requires
        # an integer subtraction.
        # The weird domain [sqrt(2)/2, sqrt(2)] works (and is used by sun's log)
        # by adding a conditional integer subtraction.
        # On the other hand, [0.5, 1.5] wouldn't really work since we easily
        # reduce to a smaller range as stated above.
        # The domain [1.0, 1.5] wouldn't work either since there is no easy way
        # to map the starting range of `m` to this domain.

        self.out_type = types.Impl(our_in_type.function,
                                   Interval("0.0", "INFINITY"))
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        # in = ...
        # k = exponent(in)
        # m = set_exponent(in, 0)
        # [optional]
        # if (m > bound):
        #     m /= 2
        #     k += 1
        # ...
        # y = ...
        # out = y + k * f(2)
        # ...
        self.type_check()
        so_far = super().generate(numeric_type=numeric_type)
        block_list = list()

        # Reduce
        red_in_name = self.gensym("mult_reduction_in")
        red_out_name = so_far[0].in_names[0]
        k = self.gensym("k")

        decomp = DecomposeFloat(numeric_type,
                                [red_in_name],
                                [red_out_name, k])
        block_list.append(decomp)

        # See above for comments about whether a domain will work
        # For now just support m in [1.0, 2.0] and [sqrt(2)/2, sqrt(2)]
        domain = self.in_node.out_type.domain
        float_domain = [domain.float_inf, domain.float_sup]
        if float_domain == [1.0, 2.0]:
            pass  # Nothing to do
        elif float_domain == [sqrt(2) / 2, sqrt(2)]:
            fold = FoldTop(numeric_type,
                           [red_out_name, k],
                           [red_out_name, k],
                           domain.sup)
            block_list.append(fold)
        else:
            logger.error("Unsupported domain: {}", float_domain)
            raise NotImplementedError("Multiplicative domains need more work")

        # Add inner blocks
        block_list.extend(so_far)

        # Reconstruct
        y = so_far[-1].out_names[0]
        rec_out_name = self.gensym("mult_recons_out")

        fpc = fpcore.parse("(FPCore (y k) (+ y (* k q)))")
        q = numeric_type.num_to_str(self.out_type.function.eval(2))
        fpc = fpc.substitute(fpcore.ast.Variable("q"),
                             fpcore.ast.Number(q))

        recons = lego_blocks.LegoFPCore(numeric_type,
                                        [y, k],
                                        [rec_out_name],
                                        fpc)
        block_list.append(recons)

        return block_list


class DecomposeFloat(lego_blocks.LegoBlock):

    def __init__(self,
                 numeric_type,
                 in_names,
                 out_names):
        super().__init__(numeric_type, in_names, out_names)
        assert len(self.in_names) == 1
        assert len(self.out_names) == 2

    def to_c(self):
        cdecl = self.numeric_type.c_type
        assert cdecl == "double", "Only double currently supported"
        # TODO: add support for float
        # TODO: should we scale denormal numbers into normals?

        df_in = self.in_names[0]
        m = self.out_names[0]
        k = self.out_names[1]

        source_lines = [
            f"int {k} = get_exponent_double({df_in}) - 1023;",
            f"{cdecl} {m} = set_exponent_double({df_in}, 1023);",
        ]
        return source_lines


class FoldTop(lego_blocks.LegoBlock):

    def __init__(self,
                 numeric_type,
                 in_names,
                 out_names,
                 bound):
        super().__init__(numeric_type, in_names, out_names)
        assert len(self.in_names) == 2
        assert self.in_names == self.out_names
        self.bound = bound

    def to_c(self):
        cdecl = self.numeric_type.c_type

        m = self.out_names[0]
        k = self.out_names[1]

        bound = self.numeric_type.num_to_str(self.bound)

        source_lines = [
            f"if ({m} < {bound}) {{",
            f"    {k} += 1;",
            f"    {m} /= 2;",
            "}"
        ]

        return source_lines
