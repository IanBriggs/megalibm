

import json
from os import path
import shlex
import subprocess
import tempfile
import fpcore
from interval import Interval
from utils.logging import Logger
from utils.timing import Timer

logger = Logger(level=Logger.HIGH, color=Logger.green)
timer = Timer()


TIMEOUT = 60 * 5


class TimeoutDirtyInfNorm(Exception):
    def __init__(self, func, domain):
        self.func = func
        self.domain = domain

    def __str__(self):
        return "\n".join([f"Func: {self.func}",
                          f"Domain: {self.domain}"])


def DirtyInfNorm(poly: fpcore.ast.ASTNode,
                 fpc: fpcore.ast.ASTNode,
                 domain: Interval,
                 prec: int = 156,
                 points: int = 501):
    poly_vars = list(poly.get_variables())
    assert len(poly_vars) == 1
    poly_var = poly_vars[0]

    fpc_vars = list(fpc.get_variables())
    assert len(fpc_vars) == 1
    fpc_var = fpc_vars[0]

    if poly_var != fpc_var:
        fpc = fpc.substitute(fpc_var, poly_var)

    sollya_poly = poly.to_sollya()
    sollya_fpc = fpc.to_sollya()
    sollya_inf = domain.inf.to_sollya()
    sollya_sup = domain.sup.to_sollya()
    lines = [
        f"prec = {prec}!;",
        f"points = {points}!;",
        f"p = {sollya_poly};",
        f"f = {sollya_fpc};",
        f"I = [{sollya_inf};{sollya_sup}];",
        f"din = dirtyinfnorm(f-p, I);",
        'print("{");',
        'print("  \\"din\\" : "@din);',
        'print("}");',
        'quit;'
    ]
    query = "\n".join(lines)

    query_name = "din.sollya"
    with tempfile.TemporaryDirectory("w") as my_dir:

        # Write out the query
        with open(path.join(my_dir, query_name), "w") as f:
            f.write(query)
            f.flush()

        # Put together the Sollya command
        run_command = "sollya --flush --warnonstderr {}".format(query_name)
        logger("Command: '{}'", run_command)
        logger.blog("Query", query)

        # Call Sollya
        with subprocess.Popen(shlex.split(run_command),
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              cwd=my_dir) as p:

            # Make sure that the run is complete and grab output
            # todo: should there be a timeout? yes....
            try:
                raw_out, raw_err = p.communicate(timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                p.kill()
                logger.warning("Timeout reached, killing Sollya")
                raise TimeoutDirtyInfNorm(fpc_or_expr,
                                              domain)

            stdout = raw_out.decode("utf8").strip()
            stderr = raw_err.decode("utf8").strip()
            returncode = p.returncode

            logger.blog("stdout", stdout)
            if stderr != "":
                logger.warning("Sollya printed to stderr")
                logger.blog("stderr", stderr)
            logger("Return code: {}", returncode)

    data = json.loads(stdout)
    return data["din"]
