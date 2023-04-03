
import fpcore
from interval import Interval
from utils import Timer, Logger

import mpmath

logger = Logger(Logger.LOW, color=Logger.blue, def_color=Logger.cyan)
timer = Timer()

def dirty_equal(a: fpcore.ast.ASTNode, b: fpcore.ast.ASTNode,
                      domain: Interval):
    """
    Horrible hack of evaluating two functions at high precision to determine
    equality
    """
    timer.start()

    if type(a) == fpcore.ast.FPCore:
        a = a.body
    if type(b) == fpcore.ast.FPCore:
        b = b.body

    logger("comparing a: {}", a)
    logger("     with b: {}", b)

    old_prec = mpmath.mp.prec
    mpmath.mp.prec = 1024

    inf = domain.inf.eval()
    if not mpmath.isfinite(inf):
        inf = mpmath.mpf("1e300")

    sup = domain.sup.eval()
    if not mpmath.isfinite(sup):
        sup = mpmath.mpf("1e300")

    if not try_point(a, b, inf):
        return False

    if not try_point(a, b, sup):
        return False

    width = sup - inf
    samples = 1_000
    for _ in range(samples):
        point = inf + mpmath.rand() * width
        while point < inf or sup < point:
            point = inf + mpmath.rand() * width

        if not try_point(a, b, point):
            return False

    mpmath.mp.prec = old_prec
    elapsed = timer.stop()

    print(f"Time to test equality: {elapsed} sec")

    return True

def try_point(a: fpcore.ast.ASTNode, b: fpcore.ast.ASTNode, point: mpmath.mpf):
    a_out = a.eval(assignment={"x": point})
    b_out = b.eval(assignment={"x": point})

    lost_bits = 4
    bound = mpmath.power(2, -(mpmath.mp.prec-lost_bits))

    abs_diff = abs(a_out - b_out)

    # Early out for close enough answers
    if abs_diff < bound:
        return True

    # If the true value is zero and we did not take the early out
    # then return False
    if a_out == 0.0:
        logger("Unequal at point: {}", point)
        logger("a(point): {}", point)
        logger("b(point): {}", point)
        logger("difference: {}", abs_diff)
        return False

    # Otherwise use relative difference
    rel_diff = abs_diff / abs(a_out)
    res = rel_diff < bound
    if not res:
        logger("Unequal at point: {}", point)
        logger("a(point): {}", point)
        logger("b(point): {}", point)
        logger("difference: {}", abs_diff)
        logger("relative_diff: {}", rel_diff)
    return res

