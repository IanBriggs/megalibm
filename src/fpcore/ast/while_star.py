

from .while_loop import While
from .ast_utils import list_to_str

from utils import Logger


logger = Logger(level=Logger.EXTRA)




class WhileStar(While):
    def __str__(self):
        format_str = super().__str__()
        bindings_str = list_to_str(self.update_bindings)
        this_str = "(while* {} ({}) {})".format(self.cond,
                                                bindings_str,
                                                self.body)
        return format_str.format(this_str)
