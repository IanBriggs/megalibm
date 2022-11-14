import math
from fpcore.ast import Variable
import lego_blocks
import numeric_types
import lambdas

from lambdas.narrow import Narrow
from interval import Interval
from lambdas import types
from utils import Logger

from lambdas.lambda_utils import find_mirrors, has_mirror_at

logger = Logger(level=Logger.HIGH, color=Logger.cyan)


class MirrorLeft(types.Transform):

    def __init__(self, in_node: types.Node):
        """
        Double the domain of a function implementation by mirroring on the
          left edge.

        in_node: An implementation valid on a domain that is symmetric on the
                 left edge of the domain.
        """
        super().__init__(in_node)

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return MirrorLeft(new_in_node)

    def type_check(self):
        """ Check that (mirror domain.inf) is an identity """
        self.in_node.type_check()
        our_in_type = self.in_node.out_type
        # TODO: Turn assert into exception
        assert type(our_in_type) == types.Impl

        func = our_in_type.function
        float_inf = float(our_in_type.domain.inf)

        # Its an error if the identity is not present
        if not has_mirror_at(func, float_inf):
            msg = "MirrorLeft requires that '{}' is mirrored about x={}"
            raise TypeError(msg.format(self.function, float_inf))

        # Create out type
        width = our_in_type.domain.sup - our_in_type.domain.inf
        next_domain = Interval(our_in_type.domain.inf - width,
                               our_in_type.domain.sup)

        # Remember the mirror point
        self.mirror_point = our_in_type.domain.inf
        self.domain = next_domain
        self.out_type = types.Impl(our_in_type.function, next_domain)

    def generate(self):
        # in = ...
        # if in < mirror_point:
        #   out = mirror_point - in
        # else:
        #   out = in
        # ...
        so_far = super().generate()
        in_name = self.gensym("in")
        out_name = so_far[0].in_names[0]

        float_bound = float(self.mirror_point)

        il = lego_blocks.IfLess(numeric_types.fp64(),
                                [in_name],
                                [out_name],
                                float(float_bound),
                                "({} - {})".format(float_bound, in_name),
                                in_name)

        return [il] + so_far

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) low high)
        # where (func) is mirrored at point (low+high)/2
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
        # Eg in this case the mirror point is too far to the right to achieve
        #   the full output by mirror
        # out domain:      <-----[#############################]----->
        # mirror point:                              |
        # in domain:       <-------------------------[#########]----->
        # real out domain: <---------------[#########|#########]----->
        #
        # Eg in this case the mirror point is exactly where it needs to be
        # out domain:      <-----[#############################]----->
        # mirror point:                         |
        # in domain:       <--------------------[##############]----->
        # real out domain: <-----[##############|##############]----->
        #
        # Eg in this case the mirror point pushes the out to be too wide and
        #   require narrowing
        # out domain:      <-----[#############################]----->
        # mirror point:                       |
        # in domain:       <------------------[################]----->
        # real out domain: <-[################|################]----->
        out_domain = out_type.domain
        mirrors = find_mirrors(out_type.function)
        mirrors = {t_arg for s, t_arg in mirrors if s == Variable("x")}
        new_holes = list()
        for m in mirrors:
            if not out_domain.contains(m):
                continue
            in_domain = Interval(m, out_domain.sup)
            in_type = types.Impl(out_type.function, in_domain)

            # check for [-inf, inf]
            if (math.isinf(float(out_domain.inf))
                and math.copysign(1.0, float(out_domain.inf)) == -1.0
                and math.isinf(float(out_domain.sup))
                    and math.copysign(1.0, float(out_domain.sup)) == 1.0):
                new_holes.append(MirrorLeft(lambdas.Hole(in_type)))
                continue

            # check for three cases
            low = 2*m - in_domain.sup

            # TODO: epsilon comparison
            # match
            if abs(float(low - out_domain.inf)) < 1e-16:
                new_holes.append(MirrorLeft(lambdas.Hole(in_type)))
                continue

            # too small
            if float(out_domain.inf) < float(low):
                continue

            # needs narrowing
            new_holes.append(
                Narrow(MirrorLeft(lambdas.Hole(in_type)), out_domain))

        return new_holes
