import fpcore
from interval import Interval
from lambdas import *
from numeric_types import FP64, FP32


libm_func_name = "libm_sun_asin"

lambda_function_name = "dsl_sun_asin"

input_ranges = [Interval("0", "0.5"), Interval("-1", "1")]

numeric_type = FP64

reference_filename = "sun_asin.c"

asin = fpcore.parse("(FPCore (x) (asin x))")

one_i = Interval("1", "1")
linear_cutoff = "7.450580596923828125e-9"
linear_i = Interval("0", linear_cutoff)
HPI = fpcore.parse_expr("PI_2")

lambda_expression = \
    InflectionLeft(
        SplitDomain({
            one_i: Horner(FixedPolynomial(asin, one_i, [0], [HPI])),
            linear_i: Horner(FixedPolynomial(asin, linear_i, [1], [1])),
            Interval(linear_cutoff, "1"):
                InflectionRight(
                    Horner(
                        FixedMultiPolynomial(
                            asin,
                            Interval("0", "0.5"),
                            fpcore.parse("(FPCore (x p q) (+ x (/ p q)))"),
                            [3, 5, 7, 9, 11, 13],
                            [" 1.66666666666666657415e-01",
                             "-3.25565818622400915405e-01",
                             " 2.01212532134862925881e-01",
                             "-4.00555345006794114027e-02",
                             " 7.91534994289814532176e-04",
                             " 3.47933107596021167570e-05"],
                            [0, 2, 4, 6, 8],
                            [" 1",
                             "-2.40339491173441421878e+00",
                             " 2.02094576023350569471e+00",
                             "-6.88283971605453293030e-01",
                             " 7.70381505559019352791e-02"])),
                    fpcore.parse_expr("(sqrt (/ (- 1 x) 2))"),
                    fpcore.parse_expr("(- (/ PI 2) (* 2 y))"), useDD=True),
        }),
        fpcore.parse_expr("(- x)"),
        fpcore.parse_expr("(- y)"))
