
# TODO: Figure out how to not repeat both the var name and value

def expect_type(name, var, typ):
    if type(var) != typ:
        msg = f"`{name}` should be of type `{typ}`, given: `{type(var)}`"
        raise TypeError(msg)

def expect_subclass(name, sub, cls):
    if not issubclass(type(sub), cls):
        msg = f"`{name}` should be a subclass of `{cls}`, given: `{sub}`"

def expect_implemented_class(name, cls):
    class_name = cls.__name__
    msg = f"`find_lambdas` not implemented for class '{class_name}'"

def expect_implemented(name, self):
    expect_implemented_class(name, type(self))
