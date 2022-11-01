
import snake_egg
import snake_egg_rules
from utils import Logger, Timer

logger = Logger(Logger.LOW, color=Logger.blue)


def egg_rule_to_expr(rule):
    T = type(rule)

    if T == int:
        return rule

    if T == snake_egg.Var:
        return str(rule).strip().replace("?", "").strip()

    args = (egg_rule_to_expr(a) for a in tuple(rule))
    return T(*args)


# This may be an incorrect idea
# See if you can prove a rule using the other rules
def check_for_redundant_rules(raw_rules, iter_limit=10):
    found_redundant = False
    for raw_rule in raw_rules:
        name, frm, to = raw_rule
        frm = egg_rule_to_expr(frm)
        to = egg_rule_to_expr(to)

        temp_raw_rules = raw_rules.copy()
        temp_raw_rules.remove(raw_rule)
        temp_rules = [snake_egg.Rewrite(r[1], r[2], r[0])
                      for r in temp_raw_rules]

        egraph = snake_egg.EGraph(snake_egg_rules.eval)
        egraph.add(frm)
        egraph.run(temp_rules, iter_limit=iter_limit)

        if egraph.equiv(frm, to):
            logger.warning("Redundant rule: {}", name)
            found_redundant = True

    return found_redundant

# See if you can prove one rule set only using rules from another


def check_rule_cover(new_raw_rules, old_raw_rules, iter_limit=10):
    new_rules = [snake_egg.Rewrite(r[1], r[2], r[0])
                 for r in new_raw_rules]

    my_timer = Timer()
    print("{:20}\t{:7}\t{:5}\t{}".format("Rule", "Covered", "Time", "Iters"))
    covered_count = 0
    for old_rule in old_raw_rules:
        name, frm, to = old_rule
        frm = egg_rule_to_expr(frm)
        to = egg_rule_to_expr(to)

        my_timer.start()
        egraph = snake_egg.EGraph(snake_egg_rules.eval)
        egraph.add(frm)
        covered = False
        i = 0
        for i in range(1, iter_limit+1):
            egraph.run(new_rules,
                       iter_limit=1,
                       node_limit=2**34,
                       time_limit=60)
            if egraph.equiv(frm, to):
                covered = True
                break
        elapsed = my_timer.stop()

        print(f"{name:20}\t{str(covered):7}\t{elapsed:.4f}\t{i}")

        covered_count += int(covered)

    print(f"Covered {covered_count} of {len(old_raw_rules)} rules")


# See if non-zero expressions can be rewritten as 0
def smoke_check_rules(raw_rules, iter_limit=10):
    rules = [snake_egg.Rewrite(r[1], r[2], r[0])
             for r in raw_rules]

    seen = set()
    my_timer = Timer()
    print("{:40}\t{:7}\t{:5}\t{}".format(
        "Expression", "EqZero", "Time", "Iters"))
    eq_zero_count = 0
    for raw_rule in raw_rules:
        name, frm, to = raw_rule
        frm = egg_rule_to_expr(frm)
        frm_str = str(snake_egg_rules.egg_to_fpcore(frm))

        if frm_str in seen:
            continue
        seen.add(frm_str)

        if to == 0:
            continue

        my_timer.start()
        egraph = snake_egg.EGraph(snake_egg_rules.eval)
        egraph.add(frm)
        eq_zero = False
        i = 0
        for i in range(1, iter_limit+1):
            egraph.run(rules,
                       iter_limit=1,
                       node_limit=2**34,
                       time_limit=60)
            if egraph.equiv(frm, 0):
                eq_zero = True
                break
        elapsed = my_timer.stop()

        print(f"{frm_str:40}\t{str(eq_zero):7}\t{elapsed:.4f}\t{i}")

        if eq_zero:
            egraph = snake_egg.EGraph()
            egraph.enable_explanations()
            egraph.add(frm)
            egraph.run(rules,
                       iter_limit=i,
                       node_limit=2**34,
                       time_limit=60)
            print(f"egraph size: {egraph.total_size()}")
            explanation = egraph.explain_equiv(frm, 0)
            print(explanation)

        eq_zero_count += int(eq_zero)

    print(f"EqZero {eq_zero_count} of {len(raw_rules)} rules")
