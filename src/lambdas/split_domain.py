
import lego_blocks
from interval import Interval
from lambdas import types
from numeric_types import fp64


class SplitDomain(types.Transform):

    def __init__(self, domains_to_impls: dict):
        self.domains_to_impls = domains_to_impls

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
        # * non-point intervals do not overlap
        # * cover the entire span from the lowest to highest domain value
        assert all(type(dom) == Interval
                   for dom in self.domains_to_impls.keys())
        non_point = [dom for dom in self.domains_to_impls.keys()
                     if dom.inf != dom.sup]
        non_point.sort(key=lambda dom: dom.inf)
        full_span_inf = non_point[0].inf
        full_span_sup = non_point[0].sup
        for dom in non_point[1:]:
            assert dom.inf == full_span_sup
            full_span_sup = dom.sup

        # check that the corresponding impls
        # * typecheck
        # * are valid for the corresponding domain
        # * are implementing the same function
        f = None
        for dom, impl in self.domains_to_impls.items():
            impl.type_check()
            assert impl.domain.inf <= dom.inf
            assert dom.sup <= impl.domain.sup
            if f is None:
                f = impl.out_type.function
            assert f == impl.out_type.function

        # Set the output
        self.domain = Interval(full_span_inf, full_span_sup)
        self.out_type = types.Impl(f, self.domain)
        self.type_check_done = True

    def generate(self, numeric_type=fp64):
        # There are many ways to do this.
        # Fiddling with the nesting of if statements can change speed.
        # We currently leave this to the expert after code generation.
        # What we do it first look at all point domains, then spans, both in
        # ascending order.

        # We:
        # * take in a variable, which is used as input for all inner sections.
        # * in the outer scope make a variable to hold our output
        # * each section then needs to set this variable

        split_in = self.gensym("split_in")
        split_out = self.gensym("split_out")
        domains_to_lego = {dom: impl.generate(numeric_type=numeric_type)
                           for dom, impl in self.domains_to_impls.items()}
        inner = lego_blocks.SplitDomain(numeric_type(),
                                        [split_in], [split_out],
                                        domains_to_lego)

        return [inner]