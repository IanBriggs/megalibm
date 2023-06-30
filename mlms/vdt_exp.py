import fpcore
import lambdas

from interval import Interval
from lambdas import *
from numeric_types import FP64

libm_func_name = "libm_vdt_exp"

lambda_function_name = "dsl_vdt_exp"

input_ranges = [Interval("0", "(log 2)"), Interval("0", "30"), Interval("-20", "20"), Interval("0", "50")]

numeric_type = FP64

reference_filename = "vdt_exp.c"

exp = fpcore.parse("(FPCore (x) (exp x))")

exp_poly = \
    Horner(
        FixedMultiPolynomial(
            exp,
            Interval("0",
                     "(log 2)"),
            fpcore.parse("(FPCore (x p q) (+ 1 (* 2 (/ p (- q p)))))"),
            [1, 3, 5],
            ["9.99999999999999999910E-1",
             "3.02994407707441961300E-2",
             "1.26177193074810590878E-4"],
            [0, 2, 4, 6],
            ["2.00000000000000000009E0",
             "2.27265548208155028766E-1",
             "2.52448340349684104192E-3",
             "3.00198505138664455042E-6"]),
        split=0)

lambda_expression = \
    RepeatExp(exp_poly, 18, 1)
