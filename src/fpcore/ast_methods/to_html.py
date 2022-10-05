from fpcore.ast import ASTNode, FPCore, list_to_str
from utils import add_method


@add_method(ASTNode)
def to_html(self, *args, **kwargs):
    # Make sure calling to_html leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"to_html not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(FPCore)
def to_html(self):
    name = self.get_any_name()
    name_str = "" if name is None else name + " "
    arguments_str = list_to_str(self.arguments)
    properties_str = list_to_str(self.properties, sep="\n    ")
    body_str = str(self.body)
    lines = [
        "<pre>",
        f"(FPCore {name_str}({arguments_str})",
        f"    {properties_str}",
        f"  {body_str})",
        "</pre>",
    ]
    return "\n".join(lines)
