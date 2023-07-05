import fpcore
import lambdas

from interval import Interval
from lambdas import *
from numeric_types import FP64


libm_func_name = "libm_vdt_cos"

lambda_function_name = "dsl_vdt_cos"

reference_filename = "vdt_cos.c"

numeric_type = FP64

input_ranges = [Interval("0", "(/ PI 4)"), Interval("-4", "4")]

cos = fpcore.parse("(FPCore (x) (cos x))")
sin = fpcore.parse("(FPCore (x) (sin x))")

pi_over_4 = fpcore.parse_expr("(/ PI 4)")
pi_over_2 = fpcore.parse_expr("(/ PI 2)")

neg_pi_over_4 = - pi_over_4

negate_x = fpcore.parse_expr("(- x)")
negate_y = fpcore.parse_expr("(- y)")
id_y = fpcore.parse_expr("y")

cos_poly = \
    Approx(cos, Interval(neg_pi_over_4, pi_over_4), 1e-16,
           Add(
        Polynomial({0: "1", 2: "-0.5"}),
        Polynomial(
            {
                4: "4.16666666666665929218E-2",
                6: "-1.38888888888730564116E-3",
                8: "2.48015872888517045348E-5",
                10: "-2.75573141792967388112E-7",
                12: "2.08757008419747316778E-9",
                14: "-1.13585365213876817300E-11"
            })))

sin_poly = \
    Approx(sin, Interval(neg_pi_over_4, pi_over_4), 1e-16,
           Polynomial(
               {
                   1: "1",
                   3: "-1.66666666666666307295E-1",
                   5: "8.33333333332211858878E-3",
                   7: "-1.98412698295895385996E-4",
                   9: "2.75573136213857245213E-6",
                   11: "-2.50507477628578072866E-8",
                   13: "1.58962301576546568060E-10"
               },
           split=1))


lambda_expression = \
    InflectionLeft(
        Additive(pi_over_2,
                 [
                     cos_poly,
                     Neg(sin_poly),
                     Neg(cos_poly),
                     sin_poly
                 ],
                 fpcore.parse("(FPCore (y k) y)"),
                 method="cody-waite",
                 cw_func=cos,
                 cw_bits=23,
                 cw_len=2),
        negate_x,
        id_y)
