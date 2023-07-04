import fpcore
from interval import Interval
from lambdas import *
from numeric_types import FP64, FP32


libm_func_name = "libm_amd_optimized_asinf"

lambda_function_name = "dsl_amd_optimized_asinf"

input_ranges = [Interval("0", "0.5"), Interval("-1", "1")]

numeric_type = FP64
func_type = FP32

reference_filename = "amd_optimized_asinf.c"

asin = fpcore.parse("(FPCore (x) (asin x))")

lambda_expression = \
    TypeCast(
        InflectionLeft(
            InflectionRight(
                Approx(asin, Interval("0", "0.5"), 5.96e-8,
                       Polynomial(
                           {
                               1: "1.0",
                               3: "0.1666666666666477004",
                               5: "0.07500000000417969548",
                               7: "0.04464285678140855751",
                               9: "0.03038196065035564039",
                               11: "0.0223717279703189581",
                               13: "0.01736009463784134871",
                               15: "0.01388184285963460496",
                               17: "0.01218919111033679899",
                               19: "0.00644940526689945226"
                           },
                           scheme="estrin",
                           split=1)),
                fpcore.parse_expr("(sqrt (/ (- 1 x) 2))"),
                fpcore.parse_expr("(- (/ PI 2) (* 2 y))")),
            fpcore.parse_expr("(- x)"),
            fpcore.parse_expr("(- y)")), frm=FP64, to=FP32)
