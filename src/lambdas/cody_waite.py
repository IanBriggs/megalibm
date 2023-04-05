

from better_float_cast import better_float_cast
from calculate_cody_waite_constants import calculate_cody_waite_constants
from dirty_equal import dirty_equal
import fpcore
from fpcore.ast import Number, Operation, Variable
import lego_blocks
from numeric_types import fp64 
import lambdas

from interval import Interval
from lambdas import types
from utils import Logger

from lambdas.lambda_utils import find_periods, has_period


logger = Logger(level=Logger.HIGH)


class CodyWaite(types.Transform):

    def __init__(self,
                 in_node: types.Node,
                 constant: fpcore.ast.Expr,
                 mod_cases: dict,
                 bits_per: int,
                 entries: int):
        """
        Infinitely expand the domain of an implementation using additive range
          reduction, starting at the left edge of the domain.

        in_node: An implementation valid on a domain with width larger than the
                 period
        period: A period of the function
        """
        self.constant = constant
        self.mod_cases = mod_cases
        self.bits_per = bits_per
        self.entries = entries
        super().__init__(in_node)

    def __str__(self):
        inner = str(self.in_node)
        return f"(AbstractPeriodic {self.constant} {inner})"

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        new_cases = None
        if self.mod_cases is not None:
            new_cases = dict()
            for k, body in self.cases.items():
                new_cases[k] = body.replace_lambda(search, replace)
        return self.__class__(new_in_node,
                              constant=self.constant,
                              mod_cases=new_cases,
                              reconstruction=self.reconstruction)

    def type_check(self):
        """
        Check that the function has the stated period and the implementation
          has the required width.
        """
        # Check normal out, when there is mod cases present then this just
        # tells us the type
        target_function = self.in_node
        float_period = better_float_cast(self.constant)

        # assert has_period(target_function, float_period)

        # Check mod cases.
        # This is when we do the reduction and have different core expressions
        # based on the mod of the "k" value

        # Check that the keys are a continuous integer sequence from 0 to n
        # The mod we will use is n+1
        mod = len(self.mod_cases)
        self.mod = mod
        assert set(range(mod)) == set(self.mod_cases.keys())

        for n, body in self.mod_cases.items():
            body.type_check()

            #TODO: Turn assert into exception
            assert type(body.out_type) == types.Impl, type(body.out_type)
            #assert has_period(body.out_type.function, float_period)
            assert better_float_cast(body.out_type.domain.width()) >= float_period, better_float_cast(body.out_type.domain.width())

            # Prove equality for each mod section
            # Given:
            #   f = target function
            #   c = constant
            #   m = mod value
            #   g = case function
            #
            # The reduction done is equivalent to:
            # y = f(x)
            #  ==>
            # k = floor(x/c)
            # w = x - k*c
            # j = k % m
            #          / j==0 -> g_0(w)
            #         |  j==1 -> g_1(w)
            # f(x) =  /  j==2 -> g_2(w)
            #         \  j==3 -> ...
            #         |  j==(k-1) -> ...
            #          \
            #
            # So we need to prove for each case that the g(w) will be
            # equivalent to f(x)
            #
            # If we have z in [0, c] then we need to prove:
            # f(z) = g_n(z + n*c)
            #

            z = Interval("0", self.constant)
            x_plus_np = Operation("+",
                                    Variable("x"),
                                    Operation("*",
                                            Number(str(n)),
                                            self.constant))
            g_n = body.out_type.function.substitute(Variable("x"), x_plus_np)

            #print(f"testing: {target_function}")
            #print(f"vs: {g_n}")
            #assert dirty_equal(target_function, g_n, z)

        self.domain = Interval("0", "INFINITY")
        self.out_type = types.Impl(target_function,
                                   self.domain)

    def generate(self, numeric_type=fp64):
        # in = ...
        # r = cody_waite_reduce(in, inv_period, period_c, period, &k, NULL);
        # switch_out;
        # switch (k % mod) {
        #   case 0:
        #       <body_0>
        #       switch_out = ...
        #       break;
        #   case 1:
        #       <body_1>
        #       switch_out = ...
        #       break;
        # }

        cw_in = self.gensym("cw_in")
        r = self.gensym("r")
        k = self.gensym("r")

        part_0 = lego_blocks.CodyWaite(
            numeric_type(),
            [cw_in], [r, k],
            self.constant,
            self.bits_per,
            self.entries,
            self.gensym,
        )

        switch_out = self.gensym("switch_out")
        # mod_to_lego = {k: impl.generate()
        #                for k, impl in self.mod_cases.items()}

        mod_to_lego = dict()
        for n, impl in self.mod_cases.items():
            print(f"k: {n}")
            print(f"Type impl: {type(impl)}")
            genned = impl.generate()
            print(f"Pavel: {impl.generate}")
            print(f"Genned: {genned}")
            mod_to_lego[n] = genned

        part_1 = lego_blocks.ModSwitch(
            numeric_type(),
            [r, k], [switch_out],
            mod_to_lego
        )

        return [part_0, part_1]

    @classmethod
    def generate_hole(cls, out_type):
        return list()
