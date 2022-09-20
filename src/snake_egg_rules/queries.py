

import snake_egg
import snake_egg_rules

from utils import Logger

logger = Logger(level=Logger.HIGH)


def is_even(func):
    se_func = func.to_snake_egg()
    logger.dlog("Func A: {}", se_func)

    arg = func.arguments[0]
    flipped_arg = -arg
    flipped = func.substitute(arg, flipped_arg)
    se_flipped = flipped.to_snake_egg()
    logger.dlog("Func B: {}", se_flipped)

    egraph = snake_egg.EGraph()
    eg_func = egraph.add(se_func)
    eg_flipped = egraph.add(se_flipped)

    for _ in range(10):
        egraph.run(snake_egg_rules.rules, iter_limit=1)
        is_even = egraph.equiv(se_func, se_flipped)
        if is_even:
            break

    logger.dlog("Is even: {}", is_even)
    return is_even


def is_odd(func):
    se_func = func.to_snake_egg()
    logger.dlog("Func A: {}", se_func)

    arg = func.arguments[0]
    flipped_arg = -arg
    flipped = func.substitute(arg, flipped_arg)
    negated = -flipped
    se_negated = negated.to_snake_egg()
    logger.dlog("Func B: {}", se_negated)

    egraph = snake_egg.EGraph()
    eg_func = egraph.add(se_func)
    eg_negated = egraph.add(se_negated)

    for _ in range(10):
        egraph.run(snake_egg_rules.rules, iter_limit=1)
        is_odd = egraph.equiv(se_func, se_negated)
        if is_odd:
            break

    logger.dlog("Is odd: {}", is_odd)
    return is_odd


def is_symmetric(func, low, middle, high):
    se_func = func.to_snake_egg()
    logger.dlog("Func: {}", se_func)

    arg = func.arguments[0]
    flipped_arg = high - arg
    flipped = func.substitute(arg, flipped_arg)
    se_flipped = flipped.to_snake_egg()
    logger.dlog("Flipped: {}", se_flipped)

    egraph = snake_egg.EGraph()
    eg_func = egraph.add(se_func)
    eg_flipped = egraph.add(se_flipped)

    egraph.run(snake_egg_rules.rules, 100)
    is_symmetric = egraph.equiv(se_func, se_flipped)
    logger.dlog("Is symmetric: {}", is_symmetric)

    return is_symmetric


def has_period(func, period):
    se_func = func.to_snake_egg()
    logger.dlog("Func: {}", se_func)

    arg = func.arguments[0]
    flipped_arg = period + arg
    flipped = func.substitute(arg, flipped_arg)
    se_flipped = flipped.to_snake_egg()
    logger.dlog("Flipped: {}", se_flipped)

    egraph = snake_egg.EGraph()
    eg_func = egraph.add(se_func)
    eg_flipped = egraph.add(se_flipped)

    egraph.run(snake_egg_rules.rules, 100)
    has_period = egraph.equiv(se_func, se_flipped)
    logger.dlog("Has period: {}", has_period)

    return has_period


def is_negation(func, low, middle, high):
    se_func = func.to_snake_egg()
    logger.dlog("Func: {}", se_func)

    arg = func.arguments[0]
    flipped_arg = high - arg
    flipped = func.substitute(arg, flipped_arg)
    negated = - flipped
    se_negated = negated.to_snake_egg()
    logger.dlog("Negated: {}", se_negated)

    egraph = snake_egg.EGraph()
    eg_func = egraph.add(se_func)
    eg_negated = egraph.add(se_negated)

    egraph.run(snake_egg_rules.rules, 100)
    is_negation = egraph.equiv(se_func, se_negated)
    logger.dlog("Is negation: {}", is_negation)

    return is_negation
