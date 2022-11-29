from fpcore.ast import Variable
import lego_blocks
import numeric_types
# import interval
import lambdas


import snake_egg
import snake_egg_rules

from interval import Interval
from lambdas import types
from snake_egg_rules import operations
from utils import Logger
import mpmath
from lambdas.lambda_utils import find_periods, has_period


logger = Logger(level=Logger.HIGH)


class InductiveRecons(types.Transform):

    def __init__(self, in_node: types.Node, period, s_expr):
        """
        Infinitely expand the domain of an implementation using additive range
          reduction, starting at the left edge of the domain.

        in_node: An implementation valid on a domain with width larger than the
                 period
        period: A period of the function
        """
        self.s_expr = s_expr
        self.period = period
        super().__init__(in_node)

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return InductiveRecons(new_in_node, period=self.period, s_expr=self.s_expr)

    def type_check(self):
        """
        Check that the function has the stated period and the implementation
          has the required width.
        """
        self.in_node.type_check()
        our_in_type = self.in_node.out_type

        float_period = float(self.period)

        #TODO: Turn assert into exception
        assert type(our_in_type) == types.Impl
        #TODO: Type check on periods
        # assert has_period(our_in_type.function, float_period)
        assert float(our_in_type.domain.width()) <= float_period

        self.domain = Interval("(- INFINITY)", "INFINITY")
        self.out_type = types.Impl(our_in_type.function,
                                   self.domain)

    def generate(self):
        # in = ...
        # k = floor((in-sup) / period)
        # out = in - period * k
        # ...
        so_far = super().generate()
        in_name = self.gensym("in")
        out_name = so_far[0].in_names[0]

        k = self.gensym("k")
        add = lego_blocks.SimpleAdditive(numeric_types.fp64(),
                                         [in_name],
                                         [out_name, k],
                                         self.in_node.domain.inf,
                                         self.period)

        #Eghraph 1
        egs = []
        s_expr = self.s_expr
        egraph = snake_egg.EGraph(snake_egg_rules.eval)
        egraph.enable_explanations()
        idk = egraph.add('k')
        id1 = egraph.add(1)
        egraph.union('idk', id1)
        egraph.union('k', 1)

        recons_1 = operations.recons("k")
        id_r = egraph.add(recons_1)
        s_body = s_expr.to_snake_egg(to_rule=False)
        id_s = egraph.add(s_body)
        
        
        egraph.union(recons_1, s_body)
        egs.append(egraph)


        #Egraph 2
        egraph2 = snake_egg.EGraph(snake_egg_rules.eval)
        egraph2.enable_explanations()
        idk2 = egraph2.add('k')
        id2 = egraph2.add(2)
        egraph2.union('k', 2)

        sec_order_s_expr = s_expr.substitute(Variable("x"), s_expr) 

        recons_2 = operations.recons("k")
        id_r2 = egraph2.add(recons_2)
        s_body2 = sec_order_s_expr.to_snake_egg(to_rule=False)
        id_s2 = egraph2.add(s_body2)
        egraph2.union(recons_2, s_body2)
        egs.append(egraph2)

        #Egraph3 
        egraph3 = snake_egg.EGraph(snake_egg_rules.eval)
        egraph3.enable_explanations()
        idk3 = egraph3.add('k')
        id2 = egraph3.add(3)
        egraph3.union('k', 3)
        thir_order_recons = sec_order_s_expr.substitute(Variable("x"), s_expr)
        recons_3 = operations.recons('k')
        id_r3 = egraph3.add(recons_3)
        s_body3 = thir_order_recons.to_snake_egg(to_rule = False)
        id_s3 = egraph3.add(s_body3)
        egraph3.union(recons_3, s_body3)
        egs.append(egraph3)


        for e in egs:
            e.run(snake_egg_rules.rules,
                   iter_limit=10,
                   time_limit=600,
                   node_limit=100_000,
                   use_simple_scheduler=True)

        inter = egraph.intersect(egraph2)
        expr = inter.extract(recons_1)


        return [add] + so_far

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) -INFINITY INFINITY)
        # where (func) is periodic
        if (type(out_type) != types.Impl
            or float(out_type.domain.inf) != -float("inf")
                or float(out_type.domain.sup) != float("inf")):
            return list()

        # To get this output we need as input
        # (Impl (func) low high)
        # where high-low is less than or equal to a period of func

        # Get periods and try both [0, period] and [-period/2, period/2]
        periods = find_periods(out_type.function)
        new_holes = list()
        for s, p in periods:
            if float(p) == 0.0 or s.contains_op("thefunc") or s == Variable("x"):
                continue
            if float(p) < 0.0:
                p = -p
            pos = types.Impl(out_type.function, Interval(0.0, p))
            new_holes.append(InductiveRecons(lambdas.Hole(pos), p, s))
            cen = types.Impl(out_type.function, Interval(-p/2, p/2))
            new_holes.append(InductiveRecons(lambdas.Hole(cen), p, s))

        return new_holes
