
import fpcore
from interval import Interval
from utils import Timer, Logger

import mpmath

logger = Logger(Logger.LOW, color=Logger.blue, def_color=Logger.cyan)
timer = Timer()


def dirty_equal(a: fpcore.ast.ASTNode,
                b: fpcore.ast.ASTNode,
                domain: Interval):
    """
    Horrible hack of evaluating two functions at high precision to determine
    equality
    """
    timer.start()

    # Convert full FPCores into their expression
    if type(a) == fpcore.ast.FPCore:
        a = a.body
    if type(b) == fpcore.ast.FPCore:
        b = b.body

    logger("comparing a: {}", a)
    logger("     with b: {}", b)

    # Get the variable name
    a_vars = a.get_variables()
    b_vars = b.get_variables()
    if a_vars != b_vars:
        msg = f"dirty_equal called on incompatible expressions: '{a}' and '{b}'"
        raise ValueError(msg)
    if len(a_vars) != 1:
        msg = f"dirty_equal called on expression with multiple variables: '{a}"
        raise ValueError(msg)
    variable_name = a_vars.pop()

    # 1k of bit is enough precision for anyone, right?
    old_prec = mpmath.mp.prec
    mpmath.mp.prec = 1024

    # Swap out infinity for a large number (more hacks)
    inf = domain.inf.eval()
    if not mpmath.isfinite(inf):
        inf = mpmath.mpf("1e300") * mpmath.sign(inf)

    sup = domain.sup.eval()
    if not mpmath.isfinite(sup):
        sup = mpmath.mpf("1e300") * mpmath.sign(inf)

    # This should not occur, but check it anyway
    assert inf <= sup, "Domain was upside down"

    # Test the endpoints (this gets messed up with infinity)
    if not try_point(a, b, variable_name, inf):
        return False

    if not try_point(a, b, variable_name, sup):
        return False

    # Test a bunch of points for equality
    width = sup - inf
    samples = 1_000
    for _ in range(samples):
        # Pick a point (hopefully) in range
        point = inf + mpmath.rand() * width

        # This should rarely run
        while point < inf or sup < point:
            point = inf + mpmath.rand() * width

        # Early out when a point doesn't match
        if not try_point(a, b, variable_name, point):
            mpmath.mp.prec = old_prec
            elapsed = timer.stop()
            logger("Time to refute equality: {} sec", elapsed)
            return False

    # Clean up and log
    mpmath.mp.prec = old_prec
    elapsed = timer.stop()
    logger("Time to test equality: {} sec", elapsed)

    return True


def try_point(a: fpcore.ast.ASTNode,
              b: fpcore.ast.ASTNode,
              name: str,
              point: mpmath.mpf) -> bool:
    # Run both at the current precision
    a_out = a.eval(assignment={name: point})
    b_out = b.eval(assignment={name: point})

    # We are arbitrarily okay if the answers differ by 4 bits
    lost_bits = 4
    bound = mpmath.power(2, -(mpmath.mp.prec - lost_bits))

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
