

import copy
from expect import expect_implemented, expect_implemented_class, expect_subclass, expect_type
import fpcore
from fpcore.ast import FPCore, Variable
from interval import Interval
from numeric_types import NumericType, FP64


# Each lambda has an out type of either an implantation or a polynomial

class Poly():

    def __init__(self, function, domain):
        self.function = function
        self.domain = domain

    def __str__(self):
        return "(Poly {} [{} {}])".format(str(self.function),
                                          self.domain.inf,
                                          self.domain.sup)

    def __repr__(self):
        return "Poly({}, {})".format(repr(self.function),
                                     repr(self.domain))


class Impl():

    def __init__(self, function, domain):
        self.function = function
        self.domain = domain

    def __str__(self):
        return "(Impl {} [{}, {}])".format(str(self.function),
                                           self.domain.inf,
                                           self.domain.sup)

    def __repr__(self):
        return "Impl({}, {})".format(repr(self.function),
                                     repr(self.domain))


# We want to be able to generate unique C level names
USED_NAMES = set()


class Node():
    """
    A node is an ast node for the lambda language.
    It represents both the relationship between the input type and output type
      as well as the C code generation through lego blocks.
    """

    def __init__(self, numeric_type: NumericType):
        self.numeric_type = numeric_type
        self.type_check_done = False
        self.out_type = None
        self.parent = None

    def find_lambdas(self, pred, _found=None):
        # look for all things that make `pred` True
        expect_implemented("find_lambdas", self)

    def replace_lambda(self, search, replace):
        # replace all instances of `search` with `replace`
        expect_implemented("replace_lambda", self)

    def type_check(self):
        expect_implemented("_type_check", self)

    def generate(self):
        # select lego blocks to use
        expect_implemented("generate", self)

    @classmethod
    def generate_hole(cls, out_type):
        # Given an out_type, return possible in types that this Transform
        # could use to reach that out_type
        expect_implemented_class("generate_hole", cls)

    def gensym(self, prefix):
        matched = {vn for vn in USED_NAMES if vn.startswith(prefix)}
        i = len(matched)
        name = prefix
        while name in matched:
            i += 1
            name = "{}_{}".format(prefix, i)
        USED_NAMES.add(name)
        return name


class Source(Node):

    def __init__(self,
                 function: FPCore,
                 domain: Interval,
                 numeric_type: NumericType = FP64):
        super().__init__(numeric_type)
        expect_type("function", function, FPCore)
        expect_type("domain", domain, Interval)
        #expect_subclass("numeric_type", numeric_type, NumericType)

        # TODO: determine if function is valid on domain

        self.out_type = Impl(function,
                             Interval(domain.inf.simplify(),
                                      domain.sup.simplify()))

    def find_lambdas(self, predicate, _found=None):
        # Setup default args
        if _found is None:
            _found = set()

        # Mark this node
        if predicate(self):
            _found.add(self)

        return _found

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        return copy.copy(self)

    def type_check(self):
        if self.type_check_done:
            return

        # TODO: determine if function is valid on domain

        self.type_check_done = True


class Transform(Node):

    def __init__(self,
                 in_node: Node,
                 numeric_type: NumericType = FP64):
        super().__init__(numeric_type)
        self.in_node = in_node
        in_node.parent = self

    def rewrite_to_use_var(self, expr, var):
        vars = expr.get_variables()
        if vars == {var.source}:
            return expr
        if self.parent is None:
            msg = (f"Unable to rewrite expression to just use `{var}`:\n"
                   f" expr: '{expr}'")
            raise ValueError(msg)
        return self.parent.rewrite_to_use_var(expr, var)
    
    def get_inner_variable(self, var):
        typ = type(var)
        if typ == Variable:
            return var
        elif typ == str:
            return Variable(var)
        else:
            raise ValueError(f"Unknown variable type: {typ}")

    def find_lambdas(self, pred, _found=None):
        # Setup default args
        if _found is None:
            _found = set()

        # Recurse
        self.in_node.find_lambdas(pred, _found)

        # Mark this node
        if pred(self):
            _found.add(self)

        return _found

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        new_in_node = self.in_node.replace_lambda(search, replace)
        return self.__class__(new_in_node)

    def __str__(self):
        class_name = type(self).__name__
        return "({} {})".format(class_name, str(self.in_node))

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({})".format(class_name, repr(self.in_node))

    def generate(self, numeric_type=FP64):
        return self.in_node.generate(numeric_type=numeric_type)


class VariableRequest:
    def __init__(self, var: fpcore.ast.Variable):
        self.var = var