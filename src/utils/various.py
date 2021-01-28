

from utils.logging import Logger


logger = Logger()




def parse_float(x):
    if type(x) == float:
        return x
    if type(x) == int:
        return x
    if type(x) == str:
        if "0x" in x:
            return float.fromhex(x)
        else:
            return float(x)
    logger.error("Unable to parse as float: {}", x)
