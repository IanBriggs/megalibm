

from fpcore.ast import list_to_str, FPCore, ASTNode
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def to_html(self):
    # Make sure calling to_html leads to an error if not overridden
    class_name = type(self).__name__
    msg = "to_html not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(FPCore)
def to_html(self):
    name_str = "" if self.name is None else self.name + " "
    arguments_str = list_to_str(self.arguments)
    properties_str = list_to_str(self.properties, sep="\n    ")
    body_str = str(self.body)
    return ("<pre>\n"
            "(FPCore {}({})\n"
            "    {}\n"
            "  {})\n"
            "</pre>").format(name_str,
                             arguments_str,
                             properties_str,
                             body_str)
