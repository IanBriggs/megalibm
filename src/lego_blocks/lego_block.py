

from numeric_types import NumericType


class LegoBlock():

    def __init__(self, numeric_type, in_names, out_names, *args):
        #assert(type(numeric_type) == NumericType)
        assert (all([type(n) == str for n in in_names]))
        assert (all([type(n) == str for n in out_names]))
        self.numeric_type = numeric_type
        self.in_names = in_names
        self.out_names = out_names

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({}, {}, {})".format(class_name,
                                       repr(self.in_names),
                                       repr(self.out_names))

    def to_c(self):
        raise NotImplementedError()
