

from utils.logging import Logger
from utils.timing import Timer

from os import path

import os
import shlex
import subprocess
import sys
import tempfile

EXTRA = Logger.EXTRA
logger = Logger(level=Logger.HIGH)
timer = Timer()


REQUIRED_CONFIG = {
    "--debug"                     : "false",   # true
    "--verbosity"                 : "2",       # 2
    "--print-opt-lower-bounds"    : "true",    # true
    "--print-hex-floats"          : "true",    # true
    "--print-second-order-errors" : "true",    # false
    "--all-indices"               : "true",    # true
}

DEFAULT_CONFIG = {
    # "--print-precision"         : "7",       # 7
    "--abs-error"                 : "false",   # true
    "--rel-error"                 : "false",   # false
    # "--ulp-error"               : "false",   # false
    "--rel-error-threshold"       : "0.0001",  # 0.0001
    # "--default-var-type"        : "float64", # float64
    # "--default-rnd"             : "rnd64",   # rnd64
    "--find-bounds"               : "false",   # false
    # "--uncertainty"             : "false",   # false
    "--fail-on-exception"         : "false",   # true
    # "--maxima-simplification"   : "false",   # false
    "--fp-power2-model"           : "false",   # true
    "--const-approx-real-vars"    : "false",   # false
    "--intermediate-opt"          : "false",   # false
    "--unique-indices"            : "false",   # true
    # "--proof-record"            : "false",   # false
    # "--proof-dir"               : "proofs",  # proofs
    # "--log-base-dir"            : "log",     # log
    # "--log-append-date"         : "start",   # start
    # "--export-options"          : "my.cfg",  #
    # "--tmp-base-dir"            : "tmp",     # tmp
    # "--tmp-date"                : "false",   # false
    # "--export-error-bounds"     : "find.c",  #
    # "--export-error-bounds-data": "data.c",  #
    "--opt"                       : "gelpia",  # auto
    "--opt-approx"                : "false",   # false
    "--opt-exact"                 : "false",   # true
    "--opt-f-rel-tol"             : "0.1",     # 0.01
    "--opt-f-abs-tol"             : "0.2",     # 0.01
    "--opt-x-rel-tol"             : "0.0",     # 0.0
    "--opt-x-abs-tol"             : "0.2",     # 0.01
    "--opt-max-iters"             : "0",       # 1000000
    "--opt-timeout"               : "20",      # 10000
}

ERROR_FORM_CONFIG = {
    "--fp-power2-model"           : "false",
    "--unique-indices"            : "true",
}

CHECK_CONFIG = {
    "--abs-error"                 : "true",
    "--fp-power2-model"           : "true",
    "--intermediate-opt"          : "true",
    "--opt-exact"                 : "true",
}

CACHE = dict()

class Result():

    def __init__(self, query, config=None):
        self.query = query

        config = config or dict()
        assert(len(set(config) - set(DEFAULT_CONFIG)) == 0)
        config = {k:(config[k] if k in config else v)
                  for k,v in DEFAULT_CONFIG.items()}

        self.flags = (" ".join(["{} {}".format(k, v)
                                for k, v in sorted(config.items())])
                      + " "
                      + " ".join(["{} {}".format(k, v)
                                  for k, v in sorted(REQUIRED_CONFIG.items())]))

        key = (self.flags, self.query)
        if key in CACHE:
            cached = CACHE[key]
            self.stdout = cached.stdout
            self.stderr = cached.stderr
            self.returncode = cached.returncode
            self.result = cached.result
            return

        self.stdout = None
        self.stderr = None
        self.returncode = None

        timer.start()
        self._run()
        self._scrape_output()
        timer.stop()

        CACHE[key] = self


    def __repr__(self):
        return "Result({}, {})".format(repr(self.query), repr(self.config))


    def _run(self):
        # Open a temporary directory we can run FPTaylor in.
        # The directory will be removed upon exiting the with block
        query_name = "query.fptaylor"
        with tempfile.TemporaryDirectory("w") as mydir:

            # Write out the query
            with open(path.join(mydir, query_name), "w") as f:
                f.write(self.query)
                f.flush()

            # Put together the FPTaylor command
            run_command = "fptaylor {} {}".format(self.flags, query_name)
            logger("Command: '{}'", run_command)
            logger.blog("Query", self.query)

            # Call FPTaylor
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
                    logger.warning("FPTaylor printed to stderr")
                    logger.blog("stderr", self.stderr)
                logger("Return code: {}", self.returncode)

    def _scrape_output(self):
        # Input being scraped and current index
        lines = [l for l in self.stdout.splitlines() if l.strip() != ""]
        idx = 0

        # Output is a nested dictionary
        self.result = dict()
        self.result["bounds"] = dict()
        self.result["expressions"] = dict()

        # Match given prefix with the next line of input
        #   return None if no match
        #   return the rest of line if match
        def peek_grab(pre):
            assert(idx < len(lines))
            line = lines[idx]
            logger.llog(EXTRA, "Mathing prefix '{}' with '{}'", pre, line)
            if not line.startswith(pre):
                return None
            rest = line[len(pre):]
            return rest.strip()

        # Match given prefix with the next line of input
        #   return None if no match
        #   consume line and return rest of line on match
        def try_grab(pre):
            nonlocal idx
            rest = peek_grab(pre)
            if rest is not None:
                idx += 1
            return rest

        # Match given prefix with the next line of input
        #   panic if no match
        #   consume line and return rest of line on match
        def grab(pre):
            rest = try_grab(pre)
            assert(rest is not None)
            return rest

        # Match given prefix with next line of input
        #   panic if no match
        #   if match extract one of the following patterns (panic if none match)
        #     "<value> (low = <low>)"
        #     "<value> (low = <low>, subopt = <subopt>)"
        #     "<value> (<hex>)"
        #     "<value> (<hex>) (suboptimality = <subopt>)"
        def grab_answer(pre):
            rest = grab(pre)
            parts = rest.split()
            value = parts[0]
            if parts[1] == "(low":
                assert(parts[2] == "=")
                low = parts[3].rstrip(",)")
                if len(parts) > 4:
                    assert(parts[4] == "subopt")
                    assert(parts[5] == "=")
                    subopt = parts[6].rstrip(")")
                    return {"value": value, "low": low, "subopt": subopt}
                return {"value": value, "low": low}
            else:
                assert(parts[1][0] == "(")
                assert(parts[1][-1] == ")")
                hexfp = parts[1][1:-1]
                if len(parts) > 2:
                    assert(parts[2] == "(suboptimality")
                    assert(parts[3] == "=")
                    subopt = parts[4].rstrip(")")
                    return {"value": value, "hex": hexfp, "subopt": subopt}
                return {"value": value, "hex": hexfp}

        # Match contiguous lines of the form:
        #   "<index>: exp = <exp>: <expr>"
        # Place them in the given dict
        def grab_taylor_forms(expressions):
            nonlocal idx
            while True:
                line = lines[idx]
                logger.llog(EXTRA, "Matching taylor expression in '{}'",line)
                parts = line.split()
                index = parts[0].rstrip(":")
                try:
                    int(index)
                except ValueError:
                    break
                assert(parts[1] == "exp")
                assert(parts[2] == "=")
                exp = parts[3].rstrip(":")
                expr = " ".join(parts[4:])
                expressions[index] = {"exp": exp,
                                      "taylor_expression": expr}
                idx += 1

        # Match contiguous lines of the form:
        #   <index>: <expr>
        # Update the given dict
        def grab_original_expressions(expressions):
            nonlocal idx
            while True:
                line = lines[idx]
                logger.llog(EXTRA, "Matching source expression in '{}'", line)
                parts = line.split()
                index = parts[0].rstrip(":")
                try:
                    int(index)
                except ValueError:
                    break
                expr = " ".join(parts[1:])
                expressions[index]["source_expression"] = expr
                idx += 1

        # Match contiguous lines of the form:
        #   "<index>: exp = <exp>: <value> (low = <low>)"
        # Place them in the given dict
        def grab_delta_terms(deltas):
            nonlocal idx
            while True:
                line = lines[idx]
                logger.llog(EXTRA, "Matching delta value in '{}'", line)
                parts = line.split()
                index = parts[0].rstrip(":")
                try:
                    int(index)
                except ValueError:
                    break
                assert(parts[1] == "exp")
                assert(parts[2] == "=")
                exp = parts[3].rstrip(":")
                value = parts[4]
                assert(parts[5] == "(low")
                assert(parts[6] == "=")
                low = parts[7].rstrip(")")
                deltas[index] = {"exp": exp,
                                   "value": value,
                                   "low": low}
                idx += 1

        # This information will always be present
        self.result["version"] = grab("FPTaylor, version")
        self.result["config_file"] = grab("Loading configuration file:")
        self.result["file"] = grab("Loading:")

        # There may be no constants
        self.result["constants"] = set()
        while True:
            rest = try_grab("Variable")
            if rest is None:
                break
            parts = rest.split()
            var = parts[0]
            assert(parts[1] == "is")
            assert(parts[2] == "a")
            assert(parts[3] == "constant")
            self.result["constants"].add(var)

        # The following will always be present
        self.result["problem"] = grab("Processing:")
        grab("*************************************")
        self.result["source_expr"] = grab("Taylor form for:")
        self.result["bounds"]["conservative"] = grab("Conservative bound:")
        self.result["simplified_expr"] = grab("Simplified rounding:")
        grab("Building Taylor forms...")

        # In some cases the simplifies Taylor forms will not be printed
        # todo: When?
        if try_grab("Simplifying Taylor forms...") != None:
            grab("success")
            self.result["original_no_rounding"] = grab("v0 =")
            grab_taylor_forms(self.result["expressions"])
            grab("Corresponding original subexpressions:")
            grab_original_expressions(self.result["expressions"])
            self.result["bounds"]["initial"] = grab("bounds:")

            # If '--abs-error true' was used we have absolute error
            self.result["absolute_errors"] = dict()
            if try_grab("Computing absolute errors") is not None:
                self.result["absolute_errors"]["delta"] = dict()
                grab_delta_terms(self.result["absolute_errors"]["delta"])
                grab("Solving the exact optimization problem")
                self.result["absolute_errors"]["m1"] = grab_answer("exact bound (exp = -53):")
                self.result["absolute_errors"]["m2"] = grab("total2:")
                self.result["absolute_errors"]["total"] = grab("exact total:")

            # If '--rel-error true' was used we have relative error
            self.result["relative_errors"] = dict()
            if try_grab("Computing relative errors") is not None:
                self.result["relative_errors"]["delta"] = dict()
                grab_delta_terms(self.result["relative_errors"]["delta"])
                grab("Solving the exact optimization problem")
                self.result["relative_errors"]["m1"] = grab_answer("exact bound-rel (exp = -53):")
                self.result["relative_errors"]["m2"] = grab("total2:")
                self.result["relative_errors"]["total"] = grab("exact total-rel:")

        # These are always present
        grab("Elapsed time:")
        grab("*************************************")
        grab("-------------------------------------------------------------------------------")

        # The problem name
        prob = grab("Problem:")
        assert(prob == self.result["problem"])

        try_grab("Optimization lower bounds for error models:")

        # All the following are pairs to pick up information when calulating
        #   absolute error or relative error

        if peek_grab("The absolute error (exact) model: "):
            self.result["absolute_errors"]["final_m1"] = grab_answer("The absolute error (exact) model: ")

        if peek_grab("The relative error (exact) model: "):
            self.result["relative_errors"]["final_m1"] = grab_answer("The relative error (exact) model: ")

        try_grab("Second order error bounds:")

        if peek_grab("Second order absolute error (exact):"):
            self.result["absolute_errors"]["final_m2"] = grab_answer("Second order absolute error (exact):")

        if peek_grab("Second order relative error (exact):"):
            self.result["relative_errors"]["final_m2"] = grab_answer("Second order relative error (exact):")

        if peek_grab("Bounds (without rounding):"):
            self.result["bounds"]["real"] = grab("Bounds (without rounding):")

        if peek_grab("Bounds (floating-point):"):
            self.result["bounds"]["float"] = grab("Bounds (floating-point):")

        if peek_grab("Absolute error (exact):"):
            self.result["absolute_errors"]["final_total"] = grab_answer("Absolute error (exact):")

        if peek_grab("Relative error (exact):"):
            self.result["relative_errors"]["final_total"] = grab_answer("Relative error (exact):")

        grab("Elapsed time:")

        # All input should be consumed
        assert(idx == len(lines))




def main(argv):
    logger.set_log_level(Logger.EXTRA)
    if len(argv) == 1:
        text = sys.stdin.read()
    elif len(argv) == 2:
        with open(argv[1], "r") as f:
            text = f.read()
    if text.strip() == "":
        text = "\n".join([
            "Variables",
            "real x in [0.01,0.5];"
	    "",
            "Definitions",
            "f rnd64= x;",
            "e = rnd[64, ne, 1.02](exp(f));",
            "r rnd64= (e - 1) / f;",
            "",
            "Expressions",
            "exp1x = r;",
        ])

    config = DEFAULT_CONFIG.copy()
    config["--opt-exact"] = "true"

    config["--abs-error"] = "false"
    config["--rel-error"] = "false"
    fpr = FPTaylorResult(text, config=config)
    pprint(fpr.result)

    config["--abs-error"] = "true"
    config["--rel-error"] = "false"
    fpr = FPTaylorResult(text, config=config)
    pprint(fpr.result)

    config["--abs-error"] = "false"
    config["--rel-error"] = "true"
    fpr = FPTaylorResult(text, config=config)
    pprint(fpr.result)

    config["--abs-error"] = "true"
    config["--rel-error"] = "true"
    fpr = FPTaylorResult(text, config=config)
    pprint(fpr.result)


if __name__ == "__main__":
    from pprint import pprint

    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
