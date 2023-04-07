
import lambdas
import snake_egg_rules
import snake_egg
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)

# Don't do this, it is bad
HACK_GLOBAL_USED_IDENTITIES = set()

def synthesize(target, fuel=10):
    # clear out global set
    HACK_GLOBAL_USED_IDENTITIES.clear()

    transforms = [
        #lambdas.NegMirrorLeft,
        lambdas.MirrorLeft,
        lambdas.MirrorRight,
        lambdas.MinimaxPolynomial,
        lambdas.Horner,
        lambdas.Periodic,
        lambdas.PeriodicRecons
    ]

    # Each list item is a lambda expression with Hole elements
    completed = list()
    old_partials = [lambdas.Hole(target)]
    for i in range(fuel):
        new_partials = list()
        for partial in old_partials:
            logger("Finishing partial impl: {}", partial)
            holes = partial.find_lambdas(lambda l: type(l) == lambdas.Hole)

            # The expression had no holes,
            if len(holes) == 0:
                completed.append(partial)
                continue

            # One hole
            found_at_least_one = False
            assert len(holes) == 1
            hole = holes.pop()

            # See if any lambdas can create this hole
            for t in transforms:
                #logger("  trying: {}", t.__name__)
                hole_fillers = t.generate_hole(hole.out_type)
                for hf in hole_fillers:
                    found_at_least_one = True
                    filled = partial.replace_lambda(hole, hf)
                    logger("    filled: {}", str(filled))
                    new_partials.append(filled)

            # Complain
            if not found_at_least_one:
                logger.warning("Unable to fill hole!")

        # Update list
        old_partials = new_partials

        # Early out
        if len(old_partials) == 0:
            break

        if i == fuel-1:
            logger.warning("Ran out of fuel!")


    my_lambdas = list()
    for c in completed:
        logger("Type check on: {}", c)
        c.type_check()
        my_lambdas.append(c)

    if len(my_lambdas) > 0:
        name = {p.name: p.value for p in target.function.properties}.get("name", "NoName")
        logger("In generating {}, we used the following identities:", name)
        for iden in HACK_GLOBAL_USED_IDENTITIES:
            logger(iden)

    return my_lambdas
