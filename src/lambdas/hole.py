
from lambdas import types


class Hole(types.Source):

    def __init__(self, out_type):
        self.out_type = out_type

    def __str__(self):
        body = self.out_type.function.body
        inf = self.out_type.domain.inf
        sup = self.out_type.domain.sup
        return f"(Hole {body} [{inf} {sup}])"