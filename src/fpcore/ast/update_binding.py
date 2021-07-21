

from .ast_node import ASTNode

from utils import Logger


logger = Logger()




class UpdateBinding(ASTNode):
    def __init__(self, name, init, step):
        self.name = name
        self.init = init
        self.step = step

    def __str__(self):
        return "[{} {} {}]".format(self.name, self.init, self.step)

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = "{} {} {}".format(self.name, self.init, self.step)
        return format_repr.format(this_repr)
