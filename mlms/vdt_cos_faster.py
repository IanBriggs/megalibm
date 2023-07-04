import fpcore
import lambdas

from interval import Interval
from lambdas import *

from numeric_types import FP64

libm_func_name = "libm_vdt_cos"

lambda_function_name = "dsl_vdt_cos_faster"

input_ranges = [Interval("0", "(/ PI 4)"), Interval("-4", "4")]

reference_filename = "vdt_cos.c"

numeric_type = FP64


cos = fpcore.parse("(FPCore (x) (cos x))")
sin = fpcore.parse("(FPCore (x) (sin x))")

pi_over_4 = fpcore.parse_expr("(/ PI 4)")
pi_over_2 = fpcore.parse_expr("(/ PI 2)")

neg_pi_over_4 = - pi_over_4

negate_x = fpcore.parse_expr("(- x)")
negate_y = fpcore.parse_expr("(- y)")
id_y = fpcore.parse_expr("y")

cos_poly = \
    Estrin(
        MinimaxPolynomial(
            cos,
            Interval(neg_pi_over_4, pi_over_4),
            8
        ),
        split=1)

sin_poly = \
    Estrin(
        MinimaxPolynomial(
            sin,
            Interval(neg_pi_over_4, pi_over_4),
            8
        ),
        split=1)

periodic_cases = {
    0: cos_poly,
    1: Neg(sin_poly),
    2: Neg(cos_poly),
    3: sin_poly,
}

lambda_expression = \
    InflectionLeft(
        CodyWaite(cos,
                  pi_over_2,
                  periodic_cases,
                  53 - 30,
                  2),
        negate_x,
        id_y)
