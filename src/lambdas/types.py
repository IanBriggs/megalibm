

from interval import Interval




# Return types

class Poly():

    def __init__(self, function, domain):
        self.function = function
        self.domain = domain

    def __str__(self):
        return "Poly<{},[{},{}]>".format(self.function,
                                         self.domain.inf,
                                         self.domain.sup)

class Impl():

    def __init__(self, function, domain):
        self.function = function
        self.domain = domain

    def __str__(self):
        return "Impl<{},[{},{}]>".format(self.function,
                                         self.domain.inf,
                                         self.domain.sup)


class Tuple():

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "Tuple({},{})".format(self.a, self.b)




# lambda object types

USED_NAMES = set()

class Node():

    def __init__(self):
        raise NotImplementedError()

    def type_check(self):
        # check that in_node.out_type matches requirements and set this out_type
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

    def __init__(self, function, domain, *args):
        self.function = function
        self.domain = domain
        self.type_check()

    def type_check(self):
        assert(type(self.function) == str)
        assert(type(self.domain) == Interval)


class Transform(Node):

    def __init__(self, in_node, *args):
        self.in_node = in_node
        self.type_check()

    def type_check(self):
        pass

    def generate(self):
        return self.in_node.generate()
