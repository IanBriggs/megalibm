
import fpcore
import lambdas

from interval import Interval
from lambdas import *
from numeric_types import FP64


libm_func_name = "libm_better_dsl_amd_fast_asin"

input_ranges = [Interval("0", "0.5"), Interval("-1", "1")]

reference_filename = "amd_fast_asin.c"

numeric_type = FP64

asin = fpcore.parse("(FPCore (x) (asin x))")


linear_cutoff = "2.1491193328907396e-08"
x = fpcore.interface.var("x")

lambda_expression = \
    InflectionLeft(
        SplitDomain({
            Interval("0", linear_cutoff):
            Horner(
                FixedPolynomial(
                    asin,
                    Interval("0", linear_cutoff),
                    [1],
                    [1]
                )),
            Interval(linear_cutoff, "1"):
            InflectionRight(
                Estrin(
                    MinimaxPolynomial(
                        asin,
                        Interval(linear_cutoff, "0.5"),
                        13
                    ),
                    split=1),
                fpcore.parse_expr("(sqrt (/ (- 1 x) 2))"),
                fpcore.parse_expr("(- (/ PI 2) (* 2 y))"))}),
        fpcore.parse_expr("(- x)"),
        fpcore.parse_expr("(- y)"))
