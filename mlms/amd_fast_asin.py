import fpcore
from interval import Interval
from lambdas import *
from numeric_types import FP64

libm_func_name = "libm_amd_fast_asin"

lambda_function_name = "dsl_amd_fast_asin"

input_ranges = [Interval("0", "0.5"), Interval("-1", "1")]

numeric_type = FP64

reference_filename = "amd_fast_asin.c"

asin = fpcore.parse("(FPCore (x) (asin x))")
linear_cutoff = "1.38777878078144552146e-17"

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
                    FixedPolynomial(
                        asin,
                        Interval("0", "0.5"),
                        [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
                        ["1",
                         "0.1666666666666477004",
                         "0.07500000000417969548",
                         "0.04464285678140855751",
                         "0.03038196065035564039",
                         "0.0223717279703189581",
                         "0.01736009463784134871",
                         "0.01388184285963460496",
                         "0.01218919111033679899",
                         "0.00644940526689945226",
                         "0.01972588778568478904",
                         "-0.01651175205874840998",
                         "0.03209627299824770186", ]),
                         split=1),
                fpcore.parse_expr("(sqrt (/ (- 1 x) 2))"),
                fpcore.parse_expr("(- (/ PI 2) (* 2 y))"))}),
        fpcore.parse_expr("(- x)"),
        fpcore.parse_expr("(- y)"))

