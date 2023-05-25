from expect import expect_implemented
from fpcore.ast import ASTNode, FPCore
from utils import add_method


@add_method(ASTNode)
def get_any_name(self, *args, **kwargs):
    expect_implemented("get_any_name", self)


@add_method(FPCore)
def get_any_name(self):
    if self.name != None:
        return self.name
    # TODO: handle multiple name properties
    for p in self.properties:
        if p.name == "name":
            return p.value
    return None
