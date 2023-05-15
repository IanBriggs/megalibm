
import lambdas
import lego_blocks
import lego_blocks.forms as forms
from lambdas import types
from numeric_types import FP64


class Horner(types.Transform):

    def __init__(self,
                 in_node: types.Node,
                 split: int = 0):
        # Run Transform initialization
        super().__init__(in_node)

        # Check and save split
        if type(split) != int:
            raise ValueError(f"'split' must be an int, given: {type(split)}")
        if split < 0:
            raise ValueError(f"'split' must be positive, given: {split}")
        self.split = split

    def type_check(self):
        # Only check once
        if self.type_check_done:
            return

        # Make sure the inner lambda expression type checks first
        self.in_node.type_check()

        # Make sure that our input is a polynomial
        our_in_type = self.in_node.out_type
        if type(our_in_type) != types.Poly:
            msg = ("Horner only applies to polynomial lambda expressions,"
                   f" given: {type(our_in_type)}")
            raise ValueError(msg)

        # Check that split is logical
        # TODO: check that split can fit in the polynomial
        # for instance, a polynomial of 10 terms cannot have a split of 100

        # Set out_type and indicate that type_check has completed
        self.out_type = types.Impl(our_in_type.function,
                                   our_in_type.domain)
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        # Make sure we type check
        self.type_check()
        block_list = list()

        # Call inner generate which is needed for Sollya based polys
        self.in_node.generate(numeric_type)

        # Create the first polynomial
        g_name = self.gensym("g")
        p_name = self.gensym("p_poly")
        p = forms.Horner(numeric_type=numeric_type,
                         in_names=[g_name],
                         out_names=[p_name],
                         monomials=self.in_node.p_monomials,
                         coefficients=self.in_node.p_coefficients,
                         split=self.split)
        block_list.append(p)

        # If there is a second polynomial create it
        if len(self.in_node.q_monomials) != 0:
            q_name = self.gensym("q_poly")
            q = forms.Horner(numeric_type=numeric_type,
                             in_names=[g_name],
                             out_names=[q_name],
                             monomials=self.in_node.q_monomials,
                             coefficients=self.in_node.q_coefficients,
                             split=self.split)
            block_list.append(q)

            # Combine polynomials
            r_name = self.gensym("r_poly")
            r = lego_blocks.LegoFPCore(numeric_type=numeric_type,
                                       in_names=[g_name, p_name, q_name],
                                       out_names=[r_name],
                                       fpc=self.in_node.combiner)
            block_list.append(r)

        return block_list

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) low high)
        if type(out_type) != types.Impl or not out_type.domain.isfinite():
            return list()

        # To get this output we need as input
        # (Poly (func) low high)
        in_type = types.Poly(out_type.function, out_type.domain)
        return [Horner(lambdas.Hole(in_type)), ]
