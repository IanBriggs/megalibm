

import json
import shlex
import subprocess
import tempfile
from os import path

import fpcore
from interval import Interval
from utils.logging import Logger
from utils.timing import Timer

logger = Logger(level=Logger.HIGH, color=Logger.green)
timer = Timer()


TIMEOUT = 60 * 5
CACHE = dict()


class FailedGenError(Exception):
    def __init__(self, func, domain):
        self.func = func
        self.domain = domain


class Result():

    default_config = {
        "precision": 512,
        "analysis_bound": 2**-20,
        "minimize_target": "relative",
    }

    def __init__(self, func, domain, monomials, numeric_type,
                 config=None, is_retry=False):
        self.func = func
        self.domain = Interval(domain.inf.simplify(), domain.sup.simplify())
        self.monomials = monomials
        self.numeric_type = numeric_type
        self.config = config or Result.default_config

        self.stdout = None
        self.stderr = None
        self.returncode = None

        timer.start()

        # Default query
        self._generate_query()
        have_res = self._try_cache()
        if not have_res:
            have_res = self._try_run()

        # Try [inf - small, sup]
        if not have_res:
            logger.warning("Sollya call failed, trying [inf - small, sup] ")
            self.domain = Interval(domain.inf - fpcore.ast.Number("0.00390625"),
                                  domain.sup)
            self._generate_query()
            have_res = self._try_cache()
        if not have_res:
            have_res = self._try_run()

        # Try [inf, sup + small]
        if not have_res:
            logger.warning("Sollya call failed, trying [inf, sup + small]")
            self.domain = Interval(domain.inf,
                                  domain.sup + fpcore.ast.Number("0.00390625"))
            self._generate_query()
            have_res = self._try_cache()
        if not have_res:
            have_res = self._try_run()

        # Try [inf-small, sup + small]
        if not have_res:
            logger.warning("Sollya call failed, trying [inf, sup + small]")
            self.domain = Interval(domain.inf - fpcore.ast.Number("0.00390625"),
                                  domain.sup + fpcore.ast.Number("0.00390625"))
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
                                                   repr(self.numeric_type.name),
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
        lines = [
            'prec = {}!;'.format(self.config["precision"]),
            'algo_analysis_bound = {};'.format(self.config["analysis_bound"]),
            'I = [{};{}];'.format(
                self.domain.inf.to_sollya(), self.domain.sup.to_sollya()),
            'f = {};'.format(self.func.to_sollya()),
            'monomials = [|{}|];'.format(monomials_str),
            'formats = [|{}...|];'.format(self.numeric_type.sollya_type),
            'p = remez(f, monomials, I);',
        ]

        all_coeff = ['coeff(p,{})'.format(m) for m in self.monomials]
        fmt_coeff = '@"\\", \\""@'.join(all_coeff)

        more_lines = [
            'display = hexadecimal!;',
            'print("{");',
            'print("  \\"coefficients\\" : [\\""@{}@"\\"]");'.format(fmt_coeff),
            'print("}");',
            'quit;'
        ]

        lines.extend(more_lines)

        self.query = "\n".join(lines)

    def _run(self):
        query_name = "query.sollya"
        with tempfile.TemporaryDirectory("w") as my_dir:

            # Write out the query
            with open(path.join(my_dir, query_name), "w") as f:
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
                                  cwd=my_dir) as p:

                # Make sure that the run is complete and grab output
                # todo: should there be a timeout? yes....
                try:
                    raw_out, raw_err = p.communicate(timeout=TIMEOUT)
                except subprocess.TimeoutExpired:
                    p.kill()
                    logger.warning("Timeout reached, killing Sollya")
                    self.stdout = ""
                    self.stderr = ""
                    self.returncode = -1
                    return
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
        warning_2_part_0 = "Warning: the evaluation of the given function"
        warning_2_part_1 = "This (possibly maximum) point will be excluded from the infnorm result."
        self._replace_starting_stderr(warning_2_part_0, warning_2_part_1)

    def _replace_starting_stderr(self, start_1, start_2):
        count_1 = self.stderr.count(start_1)
        count_2 = self.stderr.count(start_2)
        assert count_1 == count_2
        if count_1 in {0, 1}:
            return
        new_error_lines = list()
        seen_part_0 = False
        seen_part_1 = False
        for line in self.stderr.splitlines():
            if line.startswith(start_1):
                if not seen_part_0:
                    new_error_lines.append(line)
                    seen_part_0 = True
                continue
            if line.startswith(start_2):
                if not seen_part_1:
                    new_error_lines.append(line)
                    new_error_lines.append(f"(repeated {count_1} times)\n")
                    seen_part_1 = True
                continue
            new_error_lines.append(line)
        self.stderr = "\n".join(new_error_lines)

    def _replace_repeats_stderr(self, warning):
        count = self.stderr.count(warning)
        if count in {0, 1}:
            return
        find = count * warning
        join = "" if warning.endswith("\n") else "\n"
        replace = warning + join + f"(repeated {count} times)\n"
        assert find in self.stderr
        self.stderr = self.stderr.replace(find, replace)

    def _parse_output(self):
        data = json.loads(self.stdout)
        for coeff in data["coefficients"]:
            if coeff == "NaN":
                raise json.JSONDecodeError("Sollya made NaN", "stdin", -1)
        self.coefficients = data["coefficients"]
