import fpcore
import lambdas

from interval import Interval
from lambdas import *

from numeric_types import FP64

libm_func_name = "libm_better_dsl_vdt_cos"

input_ranges = [Interval("0", "1.5707963267948966"), Interval("-4", "4")]

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
    Horner(
        FixedPolynomial(
            fpcore.parse(
                "(FPCore (x) (- (+ (cos x) (/ (* x x) 2)) 1))"),
            Interval(neg_pi_over_4,
                     pi_over_4),
            [0, 2, 4, 6, 8, 10, 12, 14],
            ["1",
             "-0.5",
             "4.16666666666665929218E-2",
             "-1.38888888888730564116E-3",
             "2.48015872888517045348E-5",
             "-2.75573141792967388112E-7",
             "2.08757008419747316778E-9",
             "-1.13585365213876817300E-11"]),
        split=1)

sin_poly = \
    Horner(
        FixedPolynomial(
            sin,
            Interval(neg_pi_over_4,
                     pi_over_4),
            [1, 3, 5, 7, 9, 11, 13],
            ["1",
             "-1.66666666666666307295E-1",
             "8.33333333332211858878E-3",
             "-1.98412698295895385996E-4",
             "2.75573136213857245213E-6",
             "-2.50507477628578072866E-8",
             "1.58962301576546568060E-10"]),
        split=1)

periodic_cases = {
    0: cos_poly,
    1: TransformOut(in_node=sin_poly, expr=negate_y),
    2: TransformOut(in_node=cos_poly, expr=negate_y),
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
