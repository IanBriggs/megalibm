
import numeric_types
from interval import Interval
from lambdas import types


class Hole(types.Source):

    def __init__(self, out_type):
        self.out_type = out_type
        self.function = out_type.function
        self.domain = out_type.domain
