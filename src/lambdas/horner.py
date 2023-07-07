
from expect import expect_type
from fpcore.ast import Variable
import lambdas
import lego_blocks
import lego_blocks.forms as forms
from lambdas import types
from numeric_types import FP64, FPDD, NumericType


class Horner(types.Transform):

    def __init__(self,
                 in_node: types.Node,
                 split: int = 0,
                 numeric_type: NumericType = FP64,                 
                 useDD: bool = False,
                 split_expr=None):
        # Run Transform initialization
        super().__init__(in_node, numeric_type)

        # Check and save split
        expect_type("split", split, int)
        if split < 0:
            raise ValueError(f"'split' must be positive, given: {split}")
        self.split = split
        self.useDD = useDD
        self.split_expr = split_expr


    def type_check(self):
        # Only check once
        if self.type_check_done:
            return

        # Make sure the inner lambda expression type checks first
        self.in_node.type_check()

        # Make sure that our input is a polynomial
        our_in_type = self.in_node.out_type
        expect_type("our_in_type", our_in_type, types.Poly)

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
        g = self.gensym("g")
        g_name = Variable(g)
        if self.useDD:
            gg = self.get_inner_variable(self.gensym("gg"))
            g_name = g_name.setDD(True)
        
        p = self.gensym("p_poly")
        p_name = Variable(p)
        p = forms.Horner(numeric_type=numeric_type,
                         in_names=[g_name] if not self.useDD else [g_name, gg],
                         out_names=[p],
                         monomials=self.in_node.p_monomials,
                         coefficients=self.in_node.p_coefficients,
                         split=self.split,
                         split_expr=self.split_expr)
        block_list.append(p)

        # If there is a second polynomial create it
        if len(self.in_node.q_monomials) != 0:
            q = self.gensym("q_poly")
            q_name = Variable(q)
            q = forms.Horner(numeric_type=numeric_type,
                             in_names=[g_name if not self.useDD else gg],
                             out_names=[q],
                             monomials=self.in_node.q_monomials,
                             coefficients=self.in_node.q_coefficients,
                             split=self.split)
            block_list.append(q)

            # Combine polynomials
            r_name = Variable(self.gensym("r_poly"))
            if self.useDD:
                r_name = r_name.setDD(True)

            fpc = self.in_node.combiner
            in_names = None
            if len(fpc.arguments) == 3:
                in_names = [g_name, p_name, q_name]
            else:
                in_names = [p_name, q_name]
                
            r = lego_blocks.LegoFPCore(numeric_type= FPDD if self.useDD else numeric_type,
                                       in_names=in_names,
                                       out_names=[r_name],
                                       fpc=fpc,
                                       return_type= "dd" if self.useDD else "double")
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
        return [Horner(lambdas.Hole(in_type), split=1), ]
