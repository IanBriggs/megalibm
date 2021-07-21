

from utils import Logger


logger = Logger()




def list_to_str(l, sep=" "):
    if l is None:
        return ""
    return sep.join([str(i) for i in l])


def list_to_repr(l):
    if l is None:
        return ""
    return ", ".join([repr(i) for i in l])
