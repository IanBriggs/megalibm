

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


def DirtyInfNorm(fpc_or_expr: fpcore.ast.ASTNode,
                 domain: Interval,
                 prec: int = 156,
                 points: int = 501):
    vars = list(fpc_or_expr.get_variables())
    var = vars[0]
    for old in vars[1:]:
        fpc_or_expr = fpc_or_expr.substitute(old, var)
    sollya_func = fpc_or_expr.to_sollya()
    sollya_inf = domain.inf.to_sollya()
    sollya_sup = domain.sup.to_sollya()
    lines = [
        f"prec = {prec}!",
        f"points = {points}",
        f"f = {sollya_func};"
        f"I = [{sollya_inf};{sollya_sup}];",
        f"din = dirtyinfnorm(f, I);",
        'print("{");',
        'print("  \\"din\\" : din");',
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
                stdout = ""
                stderr = ""
                returncode = -1
                raise TimeoutDirtyInfNorm(fpc_or_expr,
                                              domain)

            stdout = raw_out.decode("utf8").strip()
            stderr = raw_err.decode("utf8").strip()
            returncode = p.returncode

    data = json.loads(stdout)
    return data["din"]
