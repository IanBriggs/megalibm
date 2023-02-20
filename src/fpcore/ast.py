

from utils import Logger


logger = Logger(level=Logger.EXTRA)


# +---------------------------------------------------------------------------+
# | Helpers                                                                   |
# +---------------------------------------------------------------------------+
def list_to_str(l, sep=" "):
    if l is None:
        return ""
    return sep.join([str(i) for i in l])


def list_to_repr(l):
    if l is None:
        return ""
    return ", ".join([repr(i) for i in l])


# +---------------------------------------------------------------------------+
# | ASTNode                                                                   |
# +---------------------------------------------------------------------------+
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


# +---------------------------------------------------------------------------+
# | Expr                                                                      |
# +---------------------------------------------------------------------------+
class Expr(ASTNode):
    def __init__(self):
        super().__init__()
        self.properties = list()

    def add_properties(self, properties):
        self.properties.extend(properties)
        return self

    def __str__(self):
        if len(self.properties) == 0:
            return "{}"
        return "(! {} {{}})".format(list_to_str(self.properties))

    def __repr__(self):
        format_repr = super().__repr__()
        if len(self.properties) == 0:
            return format_repr
        props = list_to_repr(self.properties)
        prop_repr = ".add_properties([{}])".format(props)
        return format_repr + prop_repr


# +---------------------------------------------------------------------------+
# | Atom                                                                      |
# +---------------------------------------------------------------------------+
class Atom(Expr):
    def __init__(self, source):
        super().__init__()
        self.source = source

    def __str__(self):
        return super().__str__().format(self.source)

    def __repr__(self):
        return super().__repr__().format(self.source)


class Constant(Atom):
    pass


class Variable(Atom):
    def __init__(self, source):
        super().__init__(source)
        self.dimension = None

    def set_dimension(self, *dimension):
        self.dimension = dimension
        return self

    def __str__(self):
        if self.dimension is None:
            return super().__str__()
        this_str = "({} {})".format(self.source, list_to_str(self.dimension))
        return super(Expr).__str__().format(this_str)

    def __repr__(self):
        if self.dimension is None:
            return super().__repr__()
        dims = list_to_repr(self.dimension)
        dims_repr = ".set_dimension({})".format(list_to_str(self.dimension))
        return super(Expr).__repr__().format(self.source) + dims_repr

# +---------------------------------------------------------------------------+
# | Number                                                                    |
# +---------------------------------------------------------------------------+


class Number(Atom):
    def __init__(self, source):
        assert source[0] != "-"
        super().__init__(source)


class Rational(Number):
    pass


class Decnum(Number):
    pass


class Hexnum(Number):
    pass


class Digits(Number):
    def __init__(self, mantissa, exponent, base):
        self.mantissa = mantissa
        self.exponent = exponent
        self.base = base

    def __str__(self):
        this_str = "(digits {} {} {})".format(self.mantissa,
                                              self.exponent,
                                              self.base)
        return super(Expr).__str__().format(this_str)

    def __repr__(self):
        this_repr = "{}, {}, {}".format(self.mantissa,
                                        self.exponent,
                                        self.base)
        return super(Expr).__repr__().format(this_repr)


# +---------------------------------------------------------------------------+
# | Operations                                                                |
# +---------------------------------------------------------------------------+
class Operation(Expr):
    def __init__(self, op, *args):
        super().__init__()
        self.op = op
        self.args = args

    def __str__(self):
        this_str = "({} {})".format(self.op, list_to_str(self.args))
        return super().__str__().format(this_str)

    def __repr__(self):
        this_repr = "{}, {}".format(repr(self.op), list_to_repr(self.args))
        return super().__repr__().format(this_repr)


# +---------------------------------------------------------------------------+
# | If                                                                        |
# +---------------------------------------------------------------------------+
class If(Expr):
    def __init__(self, cond, true, false):
        super().__init__()
        self.cond = cond
        self.true = true
        self.false = false

    def __str__(self):
        this_str = "(if {} {} {})".format(self.cond, self.true, self.false)
        return super().__str__().format(this_str)

    def __repr__(self):
        this_repr = "{}, {}, {}".format(repr(self.cond),
                                        repr(self.true),
                                        repr(self.false))
        return super().__repr__().format(this_repr)


# +---------------------------------------------------------------------------+
# | Let                                                                       |
# +---------------------------------------------------------------------------+
class Let(Expr):
    def __init__(self, bindings, body):
        super().__init__()
        self.bindings = bindings
        self.body = body

    def __str__(self):
        this_str = "(let ({}) {})".format(list_to_str(self.bindings),
                                          self.body)
        return super().__str__().format(this_str)

    def __repr__(self):
        this_repr = "[{}], {}".format(list_to_repr(self.bindings),
                                      repr(self.body))
        return super().__repr__().format(this_repr)


class LetStar(Let):
    def __str__(self):
        this_str = "(let* ({}) {})".format(list_to_str(self.bindings),
                                           self.body)
        return super(Expr).__str__().format(this_str)


# +---------------------------------------------------------------------------+
# | While                                                                     |
# +---------------------------------------------------------------------------+
class While(Expr):
    def __init__(self, cond, update_bindings, body):
        super().__init__()
        self.cond = cond
        self.update_bindings = update_bindings
        self.body = body

    def __str__(self):
        update_bindings_str = list_to_str(self.update_bindings)
        this_str = "(while {} ({}) {})".format(self.cond,
                                               update_bindings_str,
                                               self.body)
        return super().__str__().format(this_str)

    def __repr__(self):
        update_bindings_repr = list_to_repr(self.update_bindings)
        this_repr = "{}, [{}], {}".format(repr(self.cond),
                                          update_bindings_repr,
                                          repr(self.body))
        return super().__repr__().format(this_repr)


class WhileStar(While):
    def __str__(self):
        update_bindings_str = list_to_str(self.update_bindings)
        this_str = "(while* {} ({}) {})".format(self.cond,
                                                update_bindings_str,
                                                self.body)
        return super(Expr).__str__().format(this_str)


# +---------------------------------------------------------------------------+
# | For                                                                       |
# +---------------------------------------------------------------------------+
class For(Expr):
    def __init__(self, bindings, update_bindings, body):
        super().__init__()
        self.bindings = bindings
        self.update_bindings = update_bindings
        self.body = body

    def __str__(self):
        bindings_str = list_to_str(self.bindings)
        update_bindings_str = list_to_str(self.update_bindings)
        this_str = "(for ({}) ({}) {})".format(bindings_str,
                                               update_bindings_str,
                                               self.body)
        return super().__str__().format(this_str)

    def __repr__(self):
        bindings_repr = list_to_repr(self.bindings)
        update_bindings_repr = list_to_repr(self.update_bindings)
        this_repr = "[{}], [{}], {}".format(bindings_repr,
                                            update_bindings_repr,
                                            repr(self.body))
        return super().__repr__().format(this_repr)


class ForStar(For):
    def __str__(self):
        bindings_str = list_to_str(self.bindings)
        update_bindings_str = list_to_str(self.update_bindings)
        this_str = "(for* ({}) ({}) {})".format(bindings_str,
                                                update_bindings_str,
                                                self.body)
        return super(Expr).__str__().format(this_str)


# +---------------------------------------------------------------------------+
# | Tensor                                                                    |
# +---------------------------------------------------------------------------+
class Tensor(Expr):
    def __init__(self, bindings, body):
        super().__init__()
        self.bindings = bindings
        self.body = body

    def __str__(self):
        bindings_str = list_to_str(self.bindings)
        this_str = "(tensor ({}) {})".format(bindings_str,
                                             self.body)
        return super().__str__().format(this_str)

    def __repr__(self):
        bindings_repr = list_to_repr(self.bindings)
        this_repr = "[{}], {}".format(bindings_repr,
                                      repr(self.body))
        return super().__repr__().format(this_repr)


class TensorStar(Tensor):
    def __init__(self, bindings, update_bindings, body):
        super().__init__(bindings, body)
        self.update_bindings = update_bindings

    def __str__(self):
        bindings_str = list_to_str(self.bindings)
        update_bindings_str = list_to_str(self.update_bindings)
        this_str = "(tensor* ({}) ({}) {})".format(bindings_str,
                                                   update_bindings_str,
                                                   self.body)
        return super(Expr).__str__().format(this_str)

    def __repr__(self):
        bindings_repr = list_to_repr(self.bindings)
        update_bindings_repr = list_to_repr(self.update_bindings)
        this_repr = "[{}], [{}], {}".format(bindings_repr,
                                            update_bindings_repr,
                                            repr(self.body))
        return super(Expr).__repr__().format(this_repr)


# +---------------------------------------------------------------------------+
# | Cast                                                                      |
# +---------------------------------------------------------------------------+
class Cast(Expr):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def __str__(self):
        this_str = "(cast {})".format(self.body)
        return super().__str__().format(this_str)

    def __repr__(self):
        this_repr = "{}".format(repr(self.body))
        return super().__repr__().format(this_repr)


# +---------------------------------------------------------------------------+
# | Array                                                                     |
# +---------------------------------------------------------------------------+
class Array(Expr):
    def __init__(self, items):
        super().__init__()
        self.items = items

    def __str__(self):
        items_str = list_to_str(self.items)
        this_str = "(array {})".format(items_str)
        return super().__str__().format(this_str)

    def __repr__(self):
        items_repr = list_to_repr(self.items)
        this_repr = "[{}]".format(items_repr)
        return super().__repr__().format(this_repr)


# +---------------------------------------------------------------------------+
# | Pair                                                                      |
# +---------------------------------------------------------------------------+
class Pair(ASTNode):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    def __repr__(self):
        this_repr = "{}, {}".format(repr(self.name), repr(self.value))
        return super().__repr__().format(this_repr)


class Property(Pair):
    def __str__(self):
        value_str = str(self.value)
        if type(self.value) in {tuple, list}:
            value_str = "({})".format(list_to_str(self.value))
        return ":{} {}".format(self.name, value_str)


class Binding(Pair):
    def __str__(self):
        return "[{} {}]".format(self.name, self.value)


# +---------------------------------------------------------------------------+
# | UpdateBinding                                                             |
# +---------------------------------------------------------------------------+
class UpdateBinding(ASTNode):
    def __init__(self, name, init, step):
        super().__init__()
        self.name = name
        self.init = init
        self.step = step

    def __str__(self):
        return "[{} {} {}]".format(self.name, self.init, self.step)

    def __repr__(self):
        this_repr = list_to_repr((self.name, self.init, self.step))
        return super().__repr__().format(this_repr)


# +---------------------------------------------------------------------------+
# | FPCore                                                                    |
# +---------------------------------------------------------------------------+
class FPCore(ASTNode):
    def __init__(self, name, arguments, properties, body):
        super().__init__()
        self.name = name
        self.arguments = arguments
        self.properties = properties
        self.body = body

    def __str__(self):
        name_str = "" if self.name is None else self.name + " "
        arguments_str = list_to_str(self.arguments)
        properties_str = list_to_str(self.properties)
        return "(FPCore {}({}) {} {})".format(name_str,
                                              arguments_str,
                                              properties_str,
                                              self.body)

    def __repr__(self):
        arguments_repr = list_to_repr(self.arguments)
        properties_repr = list_to_repr(self.properties)
        this_repr = "{}, [{}], [{}], {}".format(repr(self.name),
                                                arguments_repr,
                                                properties_repr,
                                                repr(self.body))
        return super().__repr__().format(this_repr)
