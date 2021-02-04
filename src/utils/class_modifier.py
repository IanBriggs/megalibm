

def add_method(aClass):
    # Decorator to add/set a member function
    def inner(func):
        setattr(aClass, func.__name__, func)
        return func
    return inner
