from fpcore.ast import ASTNode, Atom, FPCore, Operation, Variable
from utils import Logger, add_method

import template_identities

logger = Logger()


@add_method(ASTNode)
def decompose_identities(self, *args, **kwargs):
    # Make sure calling identities leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"identities not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(FPCore)
def decompose_identities(self):
    """
    Returns a dict that maps template names to a tuple of s expression and the
      float argument to the template
    """
    if not hasattr(self, "_decomposed_identities"):
        identities = template_identities.extract_identities(self)
        self._decomposed_identities = {
            "mirror": set(),
            "periodic": set(),
        }
        for iden in identities:
            opt = split_s_and_t(iden)
            if opt == None:
                logger.log("Ignoring identity: {}", iden)
                continue
            s, t_name, t_arg = opt
            self._decomposed_identities[t_name].add((s, t_arg))
    return self._decomposed_identities


def split_s_and_t(iden):
    """
    Returns None if there is not exactly one template in the identity that has
      a constant argument.
    Otherwise returns a tuple with:
      1. an expression for s (the reconstruction)
      2. the name of the t template
      3. the arg of the template as a float
    """
    templates = set()
    extract_templates(iden, templates)
    if len(templates) != 1:
        return None
    temp = templates.pop()
    s = iden.substitute(temp, Variable("x"))
    t_name = temp.op
    t_arg = temp.args[0]
    if not t_arg.is_constant():
        return None
    return s, t_name, t_arg


def extract_templates(iden, templates):
    """ Return a list of all suppressions that start with a template """
    if type(iden) != Operation:
        return
    if iden.op in {"mirror", "periodic"}:
        templates.add(iden)
    for arg in iden.args:
        extract_templates(arg, templates)
