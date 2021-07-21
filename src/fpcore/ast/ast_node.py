

from utils import Logger


logger = Logger()




class ASTNode:
    def __init__(self):
        pass

    def __str__(self):
        class_name = type(self).__name__
        msg = "__str__ is not defined for {}".format(class_name)
        raise NotImplementedError(msg)

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({{}})".format(class_name)

    def __eq__(self, other):
        class_name = type(self).__name__
        msg = "__eq__ is not defined for {}".format(class_name)
        raise NotImplementedError(msg)

    def __add__(self, other):
        class_name = type(self).__name__
        msg = "__add__ is not defined for {}".format(class_name)
        raise NotImplementedError(msg)

    def __sub__(self, other):
        class_name = type(self).__name__
        msg = "__sub__ is not defined for {}".format(class_name)
        raise NotImplementedError(msg)

    def __neg__(self):
        class_name = type(self).__name__
        msg = "__neg__ is not defined for {}".format(class_name)
        raise NotImplementedError(msg)
    
    def __float__(self):
        class_name = type(self).__name__
        msg = "__float__ is not defined for {}".format(class_name)
        raise NotImplementedError(msg)

    def substitute(self, old, new):
        class_name = type(self).__name__
        msg = "substitute is not defined for {}".format(class_name)
        raise NotImplementedError(msg)
    
    def to_wolfram(self):
        class_name = type(self).__name__
        msg = "to_wolfram is not defined for {}".format(class_name)
        raise NotImplementedError(msg)

    def to_sollya(self):
        class_name = type(self).__name__
        msg = "to_sollya is not defined for {}".format(class_name)
        raise NotImplementedError(msg)

