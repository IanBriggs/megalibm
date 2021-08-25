

from .atom import Atom

from utils import Logger


logger = Logger(level=Logger.EXTRA)




class Number(Atom):
    def __float__(self):
        return float(self.source)

    def to_wolfram(self):
        return self.source

    def to_sollya(self):
        return self.source

    def to_c(self):
        return self.source

    def to_libm_c(self):
        return self.source

    def to_mpfr_c(self, lines, temps):
        my_name = "generated_{}".format(len(temps))
        lines.append("  mpfr_set_str({}, \"{}\", 10, MPFR_RNDN);".format(my_name, self.source))
        temps.append(my_name);
        return my_name

