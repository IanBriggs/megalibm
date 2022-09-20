

from lambdas import types


class MakeTuple(types.Node):

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.type_check()

    def __repr__(self):
        return "MakeTuple({}, {})".format(repr(self.a), repr(self.b))

    def type_check(self):
        self.out_type = types.Tuple(self.a.out_type, self.b.out_type)

    def generate(self):
        ga = self.a.generate()
        gb = self.b.generate()
        return (ga, gb)

    @classmethod
    def generate_hole(cls, out_type):
        # TODO: this method
        return list()
