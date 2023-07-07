
from better_float_cast import better_float_cast
from lambdas.rewrite import Rewrite
import lego_blocks
from interval import Interval
from lambdas import types
from numeric_types import FP64


class SplitDomain(types.Transform):

    def __init__(self, domains_to_impls: dict,
                 useDD=False):
        self.domains_to_impls = domains_to_impls
        self.type_check_done = False
        self.useDD = useDD

    def __str__(self):
        pairs = list()
        for dom, impl in self.domains_to_impls.items():
            if dom.inf == dom.sup:
                dom = dom.inf
            pairs.append(f"[{str(dom)} {str(impl)}]")
        body = " ".join(pairs)
        return f"(SplitDomain {body})"

    def __repr__(self):
        return f"SplitDomain({repr(self.domains_to_impls)})"

    def find_lambdas(self, predicate, _found=None):
        # Setup default args
        if _found is None:
            _found = set()

        for impl in self.domains_to_impls.values():
            impl.find_lambdas(predicate, _found)

        # Mark this node
        if predicate(self):
            _found.add(self)

        return _found

    def replace_lambda(self, search, replace):
        new_d_to_i = dict()
        for dom, impl in self.domains_to_impls.items():
            new_impl = impl.replace_lambda(search, replace)
            new_d_to_i[dom] = new_impl
        return SplitDomain(new_d_to_i)

    def type_check(self):
        if self.type_check_done:
            return

        # check that the domains:
        # * are intervals
        # * cover the entire span from the lowest to highest domain value
        domains = sorted([dom for dom in self.domains_to_impls.keys()],
                         key=lambda i: i.float_inf)
        assert all(type(dom) == Interval for dom in domains)

        full_span_inf = min(domains, key=lambda i:i.inf).inf
        full_span_sup = max(domains, key=lambda i:i.sup).sup
        covered_interval = domains[0]
        for dom in domains[1:]:
            try:
                covered_interval = covered_interval.join(dom)
            except ValueError as e:
                raise ValueError(f"There is a gap in the covered domains.")

        # TODO: compare in a better way than casting to float64
        if (better_float_cast(full_span_inf)
            != better_float_cast(covered_interval.inf)):
            msg = (f"Expected to cover lower bound '{full_span_inf}',"
                   f" but only got to '{covered_interval.inf}'")
            raise ValueError(msg)

        if (better_float_cast(full_span_sup)
            != better_float_cast(covered_interval.sup)):
            msg = (f"Expected to cover upper bound '{full_span_sup}',"
                   f" but only got to '{covered_interval.sup}'")
            raise ValueError(msg)

        # check that the corresponding impls
        # * typecheck
        # * are valid for the corresponding domain
        # * are implementing the same function
        f = None
        for dom, impl in self.domains_to_impls.items():
            impl.type_check()
            o_dom = impl.out_type.domain
            if o_dom.inf > dom.inf or dom.sup > o_dom.sup:
                msg = ("Expected an implementation that covers"
                       f" [{dom.inf}, {dom.sup}], but it only covered"
                       f" [{o_dom.inf}, {o_dom.sup}]")
            if f is None:
                f = impl.out_type.function
            assert f == impl.out_type.function

        if self.useDD:
            for dom in self.domains_to_impls:
                impl = self.domains_to_impls[dom]
                impl.useDD = True
                if type(impl) == Rewrite:
                    impl.in_node.useDD = True
                self.domains_to_impls[dom] = impl

        # Set the output
        self.out_type = types.Impl(f, Interval(full_span_inf, full_span_sup))
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        # There are many ways to do this.
        # Fiddling with the nesting of if statements can change speed.
        # We currently leave this to the expert after code generation.
        # What we do it first look at all point domains, then spans, both in
        # ascending order.

        # We:
        # * take in a variable, which is used as input for all inner sections.
        # * in the outer scope make a variable to hold our output
        # * each section then needs to set this variable

        self.type_check()

        split_in = self.gensym("split_in")
        split_out = self.gensym("split_out")
        domains_to_lego = {dom: impl.generate(numeric_type=numeric_type)
                           for dom, impl in self.domains_to_impls.items()}
        inner = lego_blocks.SplitDomain(numeric_type,
                                        [split_in], [split_out],
                                        domains_to_lego,
                                        self.useDD)

        return [inner]
