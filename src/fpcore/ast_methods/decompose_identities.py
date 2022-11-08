import template_identities
from fpcore.ast import ASTNode, FPCore, Operation, Variable
from utils import Logger, add_method

logger = Logger()


def split_s_and_t(iden):
    """
    Returns None if there is not exactly one template in the identity that has
      a constant argument.
    Otherwise returns a tuple with:
      1. an expression for s (the reconstruction)
      2. the name of the t template
      3. the arg of the template
    """
    templates = set()
    extract_templates(iden, templates)

    # We only care if there is exactly one template
    if len(templates) != 1:
        return None
    template = templates.pop()

    # s is just the whole identity with the template replaced with x
    s = iden.substitute(template, Variable("x"))
    t_name = template.op
    t_arg = template.args[0].simplify()

    # We also only care when the template argument is constant
    if not t_arg.is_constant():
        return None

    return s, t_name, t_arg


def extract_templates(iden, templates: set):
    """
    Fill the templates sets with all sub expressions that start with a template
    """
    if type(iden) != Operation:
        return
    if iden.op in {"mirror", "periodic"}:
        templates.add(iden)
    for arg in iden.args:
        extract_templates(arg, templates)


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
      constant argument to the template.
    So if f(x) = s(f(t(x))) and we name t(x) as <template>(t_arg),
      then we get a dict from <template> names to a set of (s, t_arg) tuples.
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
