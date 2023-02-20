
from lambdas import types


class Hole(types.Source):

    def __init__(self, out_type):
        self.out_type = out_type
        self.function = out_type.function
        self.domain = out_type.domain

    def __str__(self):
        body = self.function.body
        inf = self.domain.inf
        sup = self.domain.sup
        return f"(Hole {body} [{inf} {sup}])"