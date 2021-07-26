

from error import Error
from utils.logging import Logger
from utils.timing import Timer

from os import path

import json
import shlex
import subprocess
import tempfile


logger = Logger(level=Logger.HIGH, color=Logger.green)
timer = Timer()



CACHE = dict()


class Result():

    default_config = {
        "prec" : 2**9,
        "analysis_bound" : 2**-100,
        "minmize_target" : "relative",
    }

    def __init__(self, func, domain, monomials, numeric_type, config=None):
        self.func = func
        self.domain = domain
        self.monomials = monomials
        self.numeric_type = numeric_type
        self.config = config or Result.default_config

        self.stdout = None
        self.stderr = None
        self.returncode = None

        self._generate_query()

        if self.query in CACHE:
            logger("Used cache")
            cached = CACHE[self.query]
            self.stdout = cached.stdout
            self.stderr = cached.stderr
            self.returncode = cached.returncode
            self.coefficients = cached.coefficients

        else:
            timer.start()
            self._run()
            self._parse_output()
            el = timer.stop()
            logger("Sollya time: {} sec", el)
            CACHE[self.query] = self


    def __repr__(self):
        return "Result({}, {}, {}, {}, {})".format(repr(self.func),
                                                   repr(self.domain),
                                                   repr(self.monomials),
                                                   repr(self.numeric_type),
                                                   repr(self.config))


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
            'p = fpminimax(f, monomials, formats, I, floating, absolute);',
        ]

        all_coef = ['coeff(p,{})'.format(m) for m in self.monomials]
        fmt_coef = '@"\\", \\""@'.join(all_coef)

        more_lines = [
            'display = hexadecimal!;',
            'print("{");',
            'print("  \\"coefficients\\" : [\\""@{}@"\\"]");'.format(fmt_coef),
            'print("}");',
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
            run_command = "sollya --warnonstderr {}".format(query_name)
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

                logger.blog("stdout", self.stdout)
                if self.stderr != "":
                    logger.warning("Sollya printed to stderr")
                    logger.blog("stderr", self.stderr)
                logger("Return code: {}", self.returncode)


    def _parse_output(self):
        data = json.loads(self.stdout)

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
