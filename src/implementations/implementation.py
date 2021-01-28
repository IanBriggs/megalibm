

from utils.logging import Logger


logger = Logger(level=Logger.HIGH)



USED_NAMES = set()

class Implementation():

    def __init__(self, numeric_type, *args):
        self.numeric_type = numeric_type

    def gensym(self, prefix):
        matched = {vn for vn in USED_NAMES if vn.startswith(prefix)}
        i = len(matched)
        name = "{}_{}".format(prefix, i)
        while name in matched:
            i += 1
            name = "{}_{}".format(prefix, i)
        USED_NAMES.add(name)
        return name
