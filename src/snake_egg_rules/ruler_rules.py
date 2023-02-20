
from snake_egg_rules.operations import *

from snake_egg import EGraph, Rewrite, Var, vars

x, y, z, a, b, c, d = vars("x y z a b c d")

raw_rules = [
	["0", 1, sin(div(CONST_PI(), 2))],
	["1", sin(0), 0],
	["2", add(b, a), add(a, b)],
	["3", mul(b, a), mul(a, b)],
	["4", div(a, a), 1],
	["5", sub(a, a), 0],
	["6", sub(a, 0), a],
	["7", div(a, 1), a],
	["8", a, mul(a, 1)],
	["9", a, add(a, 0)],
	["10", sub(0, a), neg(a)],
	["11", div(a, -1), neg(a)],
	["12", neg(a), mul(a, -1)],
	["13", div(0, a), 0],
	["14", mul(0, a), 0],
	["15", sub(a, -1), add(a, 1)],
	["16", sub(a, 1), add(a, -1)],
	["17", div(1, fabs(a)), fabs(div(-1, a))],
	["18", div(fabs(a), a), div(a, fabs(a))],
	["19", fabs(mul(a, a)), mul(a, a)],
	["20", fabs(fabs(a)), fabs(a)],
	["21", sub(mul(a, b), a), mul(a, add(-1, b))],
	["22", add(b, mul(b, a)), mul(b, add(1, a))],
	["23", add(1, div(b, a)), div(add(a, b), a)],
	["24", div(sub(a, b), a), sub(1, div(b, a))],
	["25", sub(b, mul(b, a)), mul(b, sub(1, a))],
	["26", mul(b, add(a, a)), mul(add(b, b), a)],
	["27", div(mul(a, b), a), b],
	["28", mul(a, div(b, a)), b],
	["29", add(a, sub(b, a)), b],
	["30", neg(add(b, a)), sub(neg(b), a)],
	["31", div(neg(b), a), neg(div(b, a))],
	["32", sub(c, sub(b, a)), sub(a, sub(b, c))],
	["33", div(c, div(b, a)), div(a, div(b, c))],
	["34", mul(c, mul(b, a)), mul(b, mul(c, a))],
	["35", sub(sub(c, b), a), sub(sub(c, a), b)],
	["36", add(c, add(b, a)), add(add(c, b), a)],
	["37", sub(c, sub(b, a)), sub(add(a, c), b)],
	["38", sub(c, sub(b, a)), add(c, sub(a, b))],
	["39", div(c, div(b, a)), div(mul(c, a), b)],
	["40", div(c, div(b, a)), mul(c, div(a, b))],
	["41", div(div(c, b), a), div(c, mul(a, b))],
	["42", sub(c, add(b, a)), sub(sub(c, a), b)],
	["43", sub(b, a), neg(sub(a, b))],
	["44", sub(b, a), add(neg(a), b)],
	["45", fabs(sub(b, a)), fabs(sub(a, b))],
	["46", div(b, neg(a)), neg(div(b, a))]]

rules = list()
for l in raw_rules:
    name = l[0]
    frm = l[1]
    to = l[2]
    rules.append(Rewrite(frm, to, name))
