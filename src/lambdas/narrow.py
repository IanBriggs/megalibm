
import lambdas.types as types
from interval import Interval
from numeric_types import fp64
from utils import Logger

logger = Logger(level=Logger.HIGH)


class Narrow(types.Transform):

    def __init__(self, in_node: types.Node, narrow_to: Interval):
        """
        Restricts the domain of an implementation to allow types to match

        in_node: An implementation valid on a domain that is larger than the
                 narrowed domain
        narrow_to: The target domain
        """
        self.narrow_to = narrow_to
        super().__init__(in_node)

    def __str__(self):
        inner = str(self.in_node)
        inf = self.narrow_to.inf
        sup = self.narrow_to.sup
        return f"(Narrow [{inf}, {sup}] {inner})"

    def __repr__(self):
        body = repr(self.in_node)
        inf = self.narrow_to.inf
        sup = self.narrow_to.sup
        return f"Narrow([{inf}, {sup}], {body})"


    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return Narrow(new_in_node, narrow_to=self.narrow_to)

    def type_check(self):
        """ Check that the domain covers the narrowed domain """
        if self.type_check_done:
            return

        self.in_node.type_check()
        our_in_type = self.in_node.out_type
        # TODO: Turn assert into exception
        assert type(our_in_type) == types.Impl

        # Check the domain
        in_domain = our_in_type.domain
        assert in_domain.contains(self.narrow_to.inf)
        assert in_domain.contains(self.narrow_to.sup)
        next_domain = self.narrow_to

        # Set the out types
        self.domain = next_domain
        self.out_type = types.Impl(our_in_type.function, next_domain)
        self.type_check_done = True

    def generate(self, numeric_type=fp64):
        return super().generate(numeric_type=numeric_type)
