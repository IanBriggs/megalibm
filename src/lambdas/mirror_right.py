
import math

import lambdas
import lego_blocks
from better_float_cast import better_float_cast
from fpcore.ast import Variable
from interval import Interval
from lambdas import types
from lambdas.lambda_utils import get_mirrors, get_mirrors_at
from lambdas.narrow import Narrow
from numeric_types import FP64
from utils import Logger

logger = Logger(level=Logger.HIGH)


class MirrorRight(types.Transform):

    def __init__(self, in_node: types.Node, s_expr):
        """
        Double the domain of a function implementation by mirroring on the
          right edge.

        in_node: An implementation valid on a domain that is symmetric on the
                 right edge of the domain.
        """
        self.s_expr = s_expr
        super().__init__(in_node)

    def __str__(self):
        inner = str(self.in_node)
        return f"(MirrorRight {self.s_expr} {inner})"

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return MirrorRight(new_in_node, self.s_expr)

    def type_check(self):
        """ Check that '<s_expr> (mirror domain.sup)' is an identity """
        if self.type_check_done:
            return

        self.in_node.type_check()
        our_in_type = self.in_node.out_type

        # TODO: Turn assert into exception
        assert type(our_in_type) == types.Impl

        func = our_in_type.function
        float_sup = better_float_cast(our_in_type.domain.sup)

        # Its an error if the identity is not present
        s_exprs = get_mirrors_at(func, float_sup)

        found_s = False
        for s_expr in s_exprs:
            if s_expr == self.s_expr:
                found_s = True
                break

        if not found_s:
            msg = "MirrorRight requires that '{}' is mirrored about x={}"
            raise TypeError(msg.format(self.function, float_sup))

        # Create out type
        width = our_in_type.domain.sup - our_in_type.domain.inf
        next_domain = Interval(our_in_type.domain.inf,
                               our_in_type.domain.sup + width)

        # Remember the mirror point
        self.mirror_point = our_in_type.domain.sup
        self.domain = next_domain
        self.out_type = types.Impl(our_in_type.function, next_domain)
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        # in = ...
        # if in < mirror_point:
        #   reduced = 2*mirror_point - in
        # else:
        #   reduced = in
        # ...
        # inner = ...
        # if in < mirror_point:
        #   recons = s(inner)
        # else:
        #   recons = inner

        # Generate the inner code first
        so_far = super().generate(numeric_type=numeric_type)
        self.type_check()

        # Reduction
        in_name = self.gensym("in")
        reduced_name = so_far[0].in_names[0]

        bound = self.mirror_point
        two_bound = better_float_cast(2 * bound)

        il_reduce = lego_blocks.IfLess(numeric_type,
                                       [in_name],
                                       [reduced_name],
                                       better_float_cast(bound),
                                       in_name,
                                       "({} - {})".format(two_bound, in_name))

        # Reconstruction
        inner_name = so_far[-1].out_names[0]
        recons_name = self.gensym("recons")
        s_expr = self.s_expr.substitute(Variable("x"), Variable(inner_name))
        s_str = s_expr.to_libm_c()

        il_recons = lego_blocks.IfLess(numeric_type,
                                       [in_name],
                                       [recons_name],
                                       better_float_cast(bound),
                                       inner_name,
                                       s_str)

        return [il_reduce] + so_far + [il_recons]

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) low high)
        # where (func) is mirrored at point inside [low, high]
        #   plus extra constraints outlined below
        if type(out_type) != types.Impl:
            return list()

        # For each mirror point we check to see if our out domain contains it.
        # Then we create the required in domain.
        # This is then used to calculate the actual out domain that would be
        #   made from the in domain.
        # From here er may decide that the mirror point and domain cause too
        #   small an output and so cannot be used, the mirror point is exactly
        #   in the center and required no modification, or the output domain is
        #   too large and requires narrowing.
        # There is a special case for infinite domains since all mirror points
        #   are valid, and infinities can screw up calculations.
        #
        # Eg in this case the mirror point is exactly where it needs to be
        # out domain:      <-----[#############################]----->
        # mirror point:                         |
        # in domain:       <-----[##############]-------------------->
        # real out domain: <-----[##############|##############]----->
        #
        # Eg in this case the mirror point is too far to the left to achieve
        #   the full output by mirror
        # out domain:      <-----[#############################]----->
        # mirror point:              |
        # in domain:       <-----[###]------------------------------->
        # real out domain: <-----[###|###]--------------------------->
        #
        # Eg in this case the mirror point means we don't gain anything from
        #   this transformation, so don't generate it
        # out domain:      <-----[#############################]----->
        # mirror point:                                        |
        # in domain:       <-----[#############################]----->
        # real out domain: <-----[#############################|#####>
        #
        # Eg in this case the mirror point pushes the out to be too wide and
        #   require narrowing
        # out domain:      <-----[#############################]----->
        # mirror point:                           |
        # in domain:       <-----[################]------------------>
        # real out domain: <-----[################|################]->
        #

        out_domain = out_type.domain
        mirrors = get_mirrors(out_type.function)
        new_holes = list()
        for reconstruction_expr, point in mirrors:
            if (point.contains_op("thefunc") or not point.is_constant()
                or not out_domain.contains(point)
                    or reconstruction_expr.contains_op("thefunc")):
                continue
            in_domain = Interval(out_domain.inf, point)
            in_type = types.Impl(out_type.function, in_domain)

            complex = {"sin", "cos", "tan"}
            if any([reconstruction_expr.contains_op(c) for c in complex]):
                continue

            # check for [-inf, inf]
            if (math.isinf(better_float_cast(out_domain.inf))
                and math.copysign(1.0, better_float_cast(out_domain.inf)) == -1.0
                and math.isinf(better_float_cast(out_domain.sup))
                    and math.copysign(1.0, better_float_cast(out_domain.sup)) == 1.0):
                new_holes.append(MirrorRight(
                    lambdas.Hole(in_type), s_expr=reconstruction_expr))
                continue

            # check for four cases
            real_out_domain = Interval(in_domain.inf,
                                       in_domain.sup + in_domain.width())

            # TODO: epsilon comparison
            # match
            if abs(better_float_cast(real_out_domain.sup - out_domain.sup)) < 1e-16:
                new_holes.append(MirrorRight(
                    lambdas.Hole(in_type), s_expr=reconstruction_expr))
                continue

            # too small
            if better_float_cast(real_out_domain.sup) < better_float_cast(out_domain.sup):
                continue

            # won't gain anything
            if abs(better_float_cast(in_domain.sup - out_domain.sup)) < 1e-16:
                continue

            # needs narrowing
            new_holes.append(
                Narrow(MirrorRight(lambdas.Hole(in_type), s_expr=reconstruction_expr), out_domain))

        return new_holes
