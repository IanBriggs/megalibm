
import mpmath


def calculate_cody_waite_constants(constant, n, kmax, floating_point_type=None):
    """
    Based on the maple function 'asplit' by Nelson Beebe in
    "The Mathematical-Function Computation Handbook" in Chapter 9 Section 1

    Given:
        constant: an FPCore constant expression
        n: the number of bits to place in each output entry
        kmax: the number of partial entries

    Return:
        C: an array of strings representing floating point numbers constructed
           such that
            + n bits of the constant are contained in each entry except the last
            + a total length of kmax + 1
    """
    # TODO: add support for floating point type

    # We will put n bits in each entry plus a full mantissa on the end.
    # As such we need at least n*kmax + mantissa bits to get this done.
    # Triple the number of bits to be safe.
    old_prec = mpmath.mp.prec
    mpmath.mp.prec = 3 * (n * kmax + 53)

    x = constant.eval({})
    base = 2  # always base 2, for now
    b = base ** n
    sum = mpmath.mpf(0)
    C = list()
    k = 0
    for k in range(1, kmax + 1):
        d = b ** k
        c = mpmath.nint((x - sum) * d)

        # TODO: output string as fp type
        next = c / d
        c_str = float.hex(float(next))
        C.append(c_str)

        sum += next

    # TODO: output string as fp type
    last = x - sum
    c_str = float.hex(float(last))
    C.append(c_str)

    mpmath.mp.prec = old_prec

    return C


if __name__ == "__main__":
    from fpcore.ast import *
    pi_over_2 = Operation("/", Constant("PI"), Number("2"))
    C = calculate_cody_waite_constants(pi_over_2, 53 - 30, 2)
    print(C)

    pi_over_4 = Operation("/", Constant("PI"), Number("4"))
    C = calculate_cody_waite_constants(pi_over_4, 53 - 30, 2)
    print(C)
