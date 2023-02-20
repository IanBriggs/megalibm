

from fpcore.ast import FPCore
from interval import Interval


# Return types

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



# lambda object types
USED_NAMES = set()


class Node():
    """
    A node is an ast node for the lambda language.
    It represents both the relationship between the input type and output type
      as well as the C code generation through lego blocks.
    """

    def __init__(self):
        raise NotImplementedError()

    def find_lambdas(self, pred, _found=None):
        # look for all things that make `pred` True
        raise NotImplementedError()

    def replace_lambda(self, search, replace):
        # replace all instances of `search` with `replace`
        raise NotImplementedError()

    def type_check_forward(self):
        # check that in_node.out_type matches requirements and set this
        # out_type
        raise NotImplementedError()

    def type_check_backward(self):
        # check that out_type can be created from this Node and set
        # in_node.out_type
        raise NotImplementedError()

    def generate(self):
        # select lego blocks to use
        raise NotImplementedError()

    def gensym(self, prefix):
        matched = {vn for vn in USED_NAMES if vn.startswith(prefix)}
        i = len(matched)
        name = "{}_{}".format(prefix, i)
        while name in matched:
            i += 1
            name = "{}_{}".format(prefix, i)
        USED_NAMES.add(name)
        return name


class Source(Node):

    def __init__(self, function: FPCore, domain: Interval):
        self.function = function
        self.domain = Interval(domain.inf.simplify(), domain.sup.simplify())
        #self.type_check()

    def find_lambdas(self, pred, _found=None):
        # Setup default args
        if _found is None:
            _found = set()

        # Mark this node
        if pred(self):
            _found.add(self)

        return _found

    def replace_lambda(self, search, replace):
        if self == search:
            return replace
        return self.copy()

    def __str__(self):
        class_name = type(self).__name__
        return "({} {} {})".format(class_name,
                                   str(self.function),
                                   str(self.domain))

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({}, {})".format(class_name,
                                   repr(self.function),
                                   repr(self.domain))

    def type_check(self):
        assert (type(self.function) == FPCore)
        assert (type(self.domain) == Interval)


class Transform(Node):

    def __init__(self, in_node: Node):
        self.in_node = in_node
        #self.type_check()

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

    @classmethod
    def generate_hole(cls, out_type):
        # Given an out_type, return possible in types that this Transform
        # could use to reach that out_type
        raise NotImplementedError()

    def __str__(self):
        class_name = type(self).__name__
        return "({} {})".format(class_name, str(self.in_node))

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({})".format(class_name, repr(self.in_node))

    def type_check(self):
        pass

    def generate(self):
        return self.in_node.generate()
