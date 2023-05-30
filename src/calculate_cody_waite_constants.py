
import mpmath

from mpmath_hex_str import mpmath_hex_str


def calculate_cody_waite_constants(constant,
                                   bits_per,
                                   entries,
                                   floating_point_type=None):
    # TODO: add support for floating point type
    assert 0 < bits_per < 54

    # We will put n bits in each entry plus a full mantissa on the end.
    # As such we need at least n*kmax + mantissa bits to get this done.
    # Triple the number of bits to be safe.
    with mpmath.workprec(3 * (bits_per * entries + 53)):
        x_mpf =  1 * constant.eval({})
        c_strs = list()
        for _ in range(entries - 1):
            with mpmath.workprec(bits_per):
                next = 1 * x_mpf
                c_str = mpmath_hex_str(next)
            c_strs.append(c_str)
            x_mpf -= next

        with mpmath.workprec(53):
            c_str = mpmath_hex_str(x_mpf)
        c_strs.append(c_str)

    return c_strs


if __name__ == "__main__":
    from fpcore.ast import *
    consts = [
        "E",
        "LN10",
        "LN2",
        "LOG10E",
        "LOG2E",
        "M_1_PI",
        "M_2_PI",
        "M_2_SQRTPI",
        "PI_2",
        "PI_4",
        "PI",
        "SQRT1_2",
        "SQRT2",
    ]
    mpmath.mp.prec = 1024

    for c in consts:
        c_expr = Constant(c)
        c_real = c_expr.eval()
        c_dd = calculate_cody_waite_constants(c_expr, 53, 2)
        err = c_real
        for s in c_dd:
            err -= float.fromhex(s)
        err = float(err)
        print(f'"{c}": "((dd) {{{c_dd[0]}, {c_dd[1]}}})", # error ~= {err}')