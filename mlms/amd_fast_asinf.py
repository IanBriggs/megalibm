import fpcore
from interval import Interval
from lambdas import *
from numeric_types import FP64, FP32

libm_func_name = "libm_amd_fast_asinf"

lambda_function_name = "dsl_amd_fast_asinf"

input_ranges = [Interval(0, 0.5), Interval(-1, 1)]

numeric_type = FP32
func_type = FP32

reference_filename = "amd_fast_asinf.c"

asin = fpcore.parse("(FPCore (x) (asin x))")

lambda_expression = \
    InflectionLeft(
        InflectionRight(
            Approx(asin, Interval("0", "0.5"), 1e-16,
                   Polynomial(
                {
                    1: "1.0",
                    3: "0.1666679084300994873",
                    5: "0.07494434714317321777",
                    7: "0.04555018618702888489",
                    9: "0.02385816909372806549",
                    11: "0.04263564199209213257"
                },
                scheme="estrin",
                split=1)),
            fpcore.parse_expr("(sqrt (/ (- 1 x) 2))"),
            fpcore.parse_expr("(- (/ PI 2) (* 2 y))")),
        fpcore.parse_expr("(- x)"),
        fpcore.parse_expr("(- y)"))
