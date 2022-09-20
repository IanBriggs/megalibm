
import lambdas

from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)


def synthesize(target, fuel=10):
    transforms = [
        lambdas.DoubleAngle,
        lambdas.RepeatFlip,
        lambdas.RepeatNegate,
        lambdas.RepeatInf,
        lambdas.FlipAboutZeroX,
        lambdas.MirrorAboutZeroX,
        lambdas.MakeTuple,
        lambdas.First,
        lambdas.Second,
        # lambdas.PuntToLibm,
        # lambdas.General,
        lambdas.Horner,
        lambdas.EvenPolynomial,
        lambdas.OddPolynomial,
    ]

    # Each list item is a tuple of what lambda calls
    completed = list()
    old_partials = [(list(), lambdas.Hole(target))]
    for i in range(fuel):
        new_partials = list()
        for so_far, p in old_partials:
            for t in transforms:
                logger("trying: {}", t)
                new_holes = t.generate_hole(p.out_type)
                for n in new_holes:
                    if type(n) == tuple:
                        logger("found match, complete type")
                        completed.append(so_far + [t, n])
                        continue
                    logger("found match, new hole: {}", n)
                    new_so_far = so_far + [t]
                    new_partials.append((new_so_far, n))
        old_partials = new_partials
        logger(old_partials)

    my_lambdas = list()
    for c in completed:
        logger("Start synth on: {}", c)
        args = c[-1]
        c.reverse()
        passes = c[1:]
        lam = passes[0](*args)
        for t in passes[1:]:
            lam = t(lam)
        logger("Finished synth")
        my_lambdas.append(lam)

    return my_lambdas
