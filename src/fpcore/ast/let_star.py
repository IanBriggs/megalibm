

from .let import Let
from .ast_utils import list_to_str

from utils import Logger


logger = Logger()




class LetStar(Let):
    def __str__(self):
        format_str = super().__str__()
        this_str = "(let* ({}) {})".format(list_to_str(self.bindings),
                                           self.body)
        return format_str.format(this_str)
