
from snake_egg_rules.operations import *

from snake_egg import EGraph, Rewrite, Var, vars

x, y, z, a, b, c, d = vars("x y z a b c d")

raw_rules = [
	["0", sub(mul(sin(a), sin(a)), mul(cos(b), cos(b))), sub(mul(sin(b), sin(b)), mul(cos(a), cos(a)))],
	["1", sub(mul(sin(a), sin(a)), mul(sin(b), sin(b))), sub(mul(cos(b), cos(b)), mul(cos(a), cos(a)))],
	["2", sub(mul(cos(b), cos(b)), mul(cos(a), cos(a))), sub(mul(sin(a), sin(a)), mul(sin(b), sin(b)))],
	["3", cos(a), cos(neg(a))],
	["4", cos(neg(a)), cos(a)],
	["5", neg(tan(a)), tan(neg(a))],
	["6", tan(neg(a)), neg(tan(a))],
	["7", neg(sin(a)), sin(neg(a))],
	["8", sin(neg(a)), neg(sin(a))],
	["9", tan(a), tan(sub(a, CONST_PI()))],
	["10", tan(sub(a, CONST_PI())), tan(a)],
	["11", sin(a), sin(sub(CONST_PI(), a))],
	["12", sin(sub(CONST_PI(), a)), sin(a)],
	["13", neg(cos(a)), cos(add(a, CONST_PI()))],
	["14", cos(add(a, CONST_PI())), neg(cos(a))],
	["15", add(cos(add(a, a)), mul(sin(a), sin(a))), mul(cos(a), cos(a))],
	["16", mul(cos(a), cos(a)), add(cos(add(a, a)), mul(sin(a), sin(a)))],
	["17", add(mul(sin(a), sin(a)), mul(cos(a), cos(a))), 1],
	["18", add(-1/2, div(cos(add(a, a)), 2)), mul(sin(neg(a)), sin(a))],
	["19", mul(sin(neg(a)), sin(a)), add(-1/2, div(cos(add(a, a)), 2))],
	["20", 0, tan(CONST_PI())],
	["21", tan(CONST_PI()), 0],
	["22", -1, cos(CONST_PI())],
	["23", cos(CONST_PI()), -1],
	["24", 0, sin(CONST_PI())],
	["25", sin(CONST_PI()), 0],
	["26", 0, tan(add(CONST_PI(), CONST_PI()))],
	["27", tan(add(CONST_PI(), CONST_PI())), 0],
	["28", 0, sin(add(CONST_PI(), CONST_PI()))],
	["29", sin(add(CONST_PI(), CONST_PI())), 0],
	["30", 1, cos(add(CONST_PI(), CONST_PI()))],
	["31", cos(add(CONST_PI(), CONST_PI())), 1],
	["32", 0, tan(0)],
	["33", tan(0), 0],
	["34", 0, sin(0)],
	["35", sin(0), 0],
	["36", 1, cos(0)],
	["37", cos(0), 1],
	["38", 1, tan(div(CONST_PI(), 4))],
	["39", tan(div(CONST_PI(), 4)), 1],
	["40", 1, sin(div(CONST_PI(), 2))],
	["41", sin(div(CONST_PI(), 2)), 1],
	["42", sin(div(CONST_PI(), 4)), cos(div(CONST_PI(), 4))],
	["43", cos(div(CONST_PI(), 4)), sin(div(CONST_PI(), 4))]]

rules = list()
for l in raw_rules:
    name = l[0]
    frm = l[1]
    to = l[2]
    rules.append(Rewrite(frm, to, name))
