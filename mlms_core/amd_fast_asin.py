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
linear_region = Interval("0", linear_cutoff)

lambda_expression = \
    InflectionLeft(
        SplitDomain({
            linear_region:
                Approx(asin, linear_region, 1e-16, Polynomial({1: "1"})),
            Interval(linear_cutoff, "1"):
            InflectionRight(
                Approx(asin, Interval("0", "0.5"), 1e-16,
                       Polynomial(
                           {
                               1: "1",
                               3: "0.1666666666666477004",
                               5: "0.07500000000417969548",
                               7: "0.04464285678140855751",
                               9: "0.03038196065035564039",
                               11: "0.0223717279703189581",
                               13: "0.01736009463784134871",
                               15: "0.01388184285963460496",
                               17: "0.01218919111033679899",
                               19: "0.00644940526689945226",
                               21: "0.01972588778568478904",
                               23: "-0.01651175205874840998",
                               25: "0.03209627299824770186"
                           },
                           scheme="estrin",
                           split=1)),
                fpcore.parse_expr("(sqrt (/ (- 1 x) 2))"),
                fpcore.parse_expr("(- (/ PI 2) (* 2 y))"))}),
        fpcore.parse_expr("(- x)"),
        fpcore.parse_expr("(- y)"))
