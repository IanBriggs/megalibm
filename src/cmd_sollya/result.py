

import math
from error import Error
from utils.logging import Logger
from utils.timing import Timer

from os import path

import fpcore
import json
import shlex
import subprocess
import tempfile
from interval import Interval

logger = Logger(level=Logger.HIGH, color=Logger.green)
timer = Timer()



CACHE = dict()


class FailedGenError(Exception):
    def __init__(self, func, domain):
        self.func = func
        self.domain = domain

class Result():

    default_config = {
        "prec" : 128,
        "analysis_bound" : 2**-20,
        "minmize_target" : "relative",
    }

    def __init__(self, func, domain, monomials, numeric_type, config=None, is_retry=False):
        self.func = func
        self.domain = domain
        self.monomials = monomials
        self.numeric_type = numeric_type
        self.config = config or Result.default_config

        self.stdout = None
        self.stderr = None
        self.returncode = None

        timer.start()
        # Defauult query
        self._generate_query()
        have_res = self._try_cache()
        if not have_res:
            have_res = self._try_run()

        # Try symmetric around domain.inf
        if not have_res:
            logger("Sollya call failed, retrying with mirrored domain")
            diff = domain.sup - domain.inf
            new_domain = Interval(domain.inf - diff, domain.sup)
            self.domain = new_domain
            self._generate_query()
            have_res = self._try_cache()
        if not have_res:
            have_res = self._try_run()

        # Try slightly asymmetric
        if not have_res:
            logger("Sollya call failed, retrying with symetric mirrored domain")
            diff = domain.sup - domain.inf
            new_domain = Interval(domain.inf - diff, domain.sup + fpcore.ast.Number("0.00390625"))
            self.domain = new_domain
            self._generate_query()
            have_res = self._try_cache()
        if not have_res:
            have_res = self._try_run()


        el = timer.stop()
        logger("Sollya time: {} sec", el)

        if not have_res:
            raise FailedGenError(func, domain)


    def __repr__(self):
        return "Result({}, {}, {}, {}, {})".format(repr(self.func),
                                                   repr(self.domain),
                                                   repr(self.monomials),
                                                   repr(self.numeric_type),
                                                   repr(self.config))

    def _try_cache(self):
        if self.query in CACHE:
            logger("Used cache")
            cached = CACHE[self.query]
            if cached == None:
                return False
            self.stdout = cached.stdout
            self.stderr = cached.stderr
            self.returncode = cached.returncode
            self.coefficients = cached.coefficients
            return True
        return False


    def _try_run(self):
        try:
            self._run()
            self._parse_output()
            CACHE[self.query] = self
            return True
        except json.decoder.JSONDecodeError:
            CACHE[self.query] = None
            return False


    def _generate_query(self):
        monomials_str = ", ".join([str(m) for m in self.monomials])
        mid = (float(self.domain.inf) + float(self.domain.sup))/2
        lines = [
            'prec = {}!;'.format(self.config["prec"]),
            'algo_analysis_bound = {};'.format(self.config["analysis_bound"]),
            'I = [{};{}];'.format(self.domain.inf.to_sollya(), self.domain.sup.to_sollya()),
            'f = {};'.format(self.func.to_sollya()),
            'monomials = [|{}|];'.format(monomials_str),
            'formats = [|{}...|];'.format(self.numeric_type.sollya_type()),
            'p = remez(f, monomials, I);',
        ]

        all_coef = ['coeff(p,{})'.format(m) for m in self.monomials]
        fmt_coef = '@"\\", \\""@'.join(all_coef)

        more_lines = [
            'display = hexadecimal!;',
            'print("{");',
            'print("  \\"coefficients\\" : [\\""@{}@"\\"]");'.format(fmt_coef),
            'print("}");',
            'quit;'
        ]

        lines.extend(more_lines)

        self.query = "\n".join(lines)


    def _run(self):
        query_name = "query.sollya"
        with tempfile.TemporaryDirectory("w") as mydir:

            # Write out the query
            with open(path.join(mydir, query_name), "w") as f:
                f.write(self.query)
                f.flush()

            # Put together the Sollya command
            run_command = "sollya --flush --warnonstderr {}".format(query_name)
            logger("Command: '{}'", run_command)
            logger.blog("Query", self.query)

            # Call Sollya
            with subprocess.Popen(shlex.split(run_command),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  cwd=mydir) as p:

                # Make sure that the run is complete and grab output
                # todo: should there be a timeout?
                raw_out, raw_err = p.communicate()
                self.stdout = raw_out.decode("utf8").strip()
                self.stderr = raw_err.decode("utf8").strip()
                self.returncode = p.returncode
                self._compress_stderr()

                logger.blog("stdout", self.stdout)
                if self.stderr != "":
                    logger.warning("Sollya printed to stderr")
                    logger.blog("stderr", self.stderr)
                logger("Return code: {}", self.returncode)

    def _compress_stderr(self):
        warning_0 = "\nWarning: at least one of the given expressions or a subexpression is not correctly typed\nor its evaluation has failed because of some error on a side-effect."
        self._replace_repeats_stderr(warning_0)
        warning_1 = "Warning: degenerated system in a non Haar context. The algorithm may be incorrect.\n"
        self._replace_repeats_stderr(warning_1)

    def _replace_repeats_stderr(self, warning):
        count = self.stderr.count(warning)
        if count == 0:
            return
        find = count * warning
        join = "" if warning.endswith("\n") else "\n"
        replace = warning + join + f"(repeated {count} times)\n"
        assert find in self.stderr
        self.stderr = self.stderr.replace(find, replace)

    def _parse_output(self):
        data = json.loads(self.stdout)
        for coef in data["coefficients"]:
            if coef == "NaN":
                raise json.JSONDecodeError("Sollya made NaN", "stdin", -1)
        self.coefficients = data["coefficients"]




def main(argv):
    logger.set_log_level(Logger.EXTRA)

    dom = Domain(0, 1.5707963267948966)
    dom.add_denormal(0, 2**-126)
    dom.add_normal(2**-126, 1.5707963267948966)

    res = SollyaResult("sin(x)", dom, [1, 3, 5, 7], FP64())

    logger("Execution time: {}".format(timer.elapsed()))


if __name__ == "__main__":
    from domain import Domain
    from numeric_types.fp64 import FP64

    import sys

    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("\nBye")

    sys.exit(retcode)
