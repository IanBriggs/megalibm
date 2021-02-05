

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
        "prec" : 2**7,
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
            self.error = cached.error

        else:
            timer.start()
            self._run()
            self._parse_output()
            timer.stop()
            logger("Sollya time: {} sec", timer.last_time())
            CACHE[self.query] = self


    def __repr__(self):
        return "Result({}, {}, {}, {}, {})".format(repr(self.func),
                                                   repr(self.domain),
                                                   repr(self.monomials),
                                                   repr(self.numeric_type),
                                                   repr(self.config))


    def _generate_query(self):
        monomials_str = ", ".join([str(m) for m in self.monomials])
        lines = [
            'prec = {}!;'.format(self.config["prec"]),
            'algo_analysis_bound = {};'.format(self.config["analysis_bound"]),
            'I = [{};{}];'.format(self.domain.inf, self.domain.sup),
            'f = {};'.format(self.func),
            'monomials = [|{}|];'.format(monomials_str),
            'p = fpminimax(f, monomials, [|{}...|], I, floating, relative);'.format(self.numeric_type.sollya_type()),
        ]

        norms = list()
        # norms = self.domain.normal_domains()
        # for i, dom in enumerate(norms):
        #     sollya_dom = "[{};{}]".format(*dom)
        #     lines.append('rel_norm_err_{} = sup(supnorm(p, f, {}, relative, algo_analysis_bound));'.format(i, sollya_dom))
        #     lines.append('abs_norm_err_{} = sup(supnorm(p, f, {}, absolute, algo_analysis_bound));'.format(i, sollya_dom))

        denorms = list()
        # denorms = self.domain.denormal_domains()
        # for i, dom in enumerate(denorms):
        #     sollya_dom = "[{};{}]".format(*dom)
        #     lines.append('rel_denorm_err_{} = sup(supnorm(p, f, {}, relative, algo_analysis_bound));'.format(i, sollya_dom))
        #     lines.append('abs_denorm_err_{} = sup(supnorm(p, f, {}, absolute, algo_analysis_bound));'.format(i, sollya_dom))

        all_coef = ['coeff(p,{})'.format(m) for m in self.monomials]
        fmt_coef = '@"\\", \\""@'.join(all_coef)

        all_rne = ['rel_norm_err_{}'.format(i) for i in range(len(norms))]
        fmt_rne = '@"\\", \\""@'.join(all_rne)
        fmt_rne = '"null"' if fmt_rne == "" else fmt_rne

        all_ane = ['abs_norm_err_{}'.format(i) for i in range(len(norms))]
        fmt_ane = '@"\\", \\""@'.join(all_ane)
        fmt_ane = '"null"' if fmt_ane == "" else fmt_ane

        all_rde = ['rel_denorm_err_{}'.format(i) for i in range(len(denorms))]
        fmt_rde = '@"\\", \\""@'.join(all_rde)
        fmt_rde = '"null"' if fmt_rde == "" else fmt_rde

        all_ade = ['abs_denorm_err_{}'.format(i) for i in range(len(denorms))]
        fmt_ade = '@"\\", \\""@'.join(all_ade)
        fmt_ade = '"null"' if fmt_ade == "" else fmt_ade

        more_lines = [
            'display = hexadecimal!;',
            'print("{");',
            'print("  \\"coefficients\\" : [\\""@{}@"\\"],");'.format(fmt_coef),
            'display = decimal!;',
            'print("  \\"relative_normal_errors\\" : [\\""@{}@"\\"],");'.format(fmt_rne),
            'print("  \\"absolute_normal_errors\\" : [\\""@{}@"\\"],");'.format(fmt_ane),
            'print("  \\"relative_denormal_errors\\" : [\\""@{}@"\\"],");'.format(fmt_rde),
            'print("  \\"absolute_denormal_errors\\" : [\\""@{}@"\\"]");'.format(fmt_ade),
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

            # Put together the FPTaylor command
            run_command = "sollya --warnonstderr {}".format(query_name)
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
                    logger.warning("Sollya printed to stderr")
                    logger.blog("stderr", self.stderr)
                logger("Return code: {}", self.returncode)


    def _parse_output(self):
        data = json.loads(self.stdout)

        self.coefficients = data["coefficients"]

        self.error = Error("Sollya")

        # for i, dom in enumerate(self.domain.normal_domains()):
        #     rel_err = data["relative_normal_errors"][i]
        #     abs_err = data["absolute_normal_errors"][i]
        #     self.error.add_normal_error(dom, abs_err, rel_err)

        # for i, dom in enumerate(self.domain.denormal_domains()):
        #     rel_err = data["relative_denormal_errors"][i]
        #     abs_err = data["absolute_denormal_errors"][i]
        #     self.error.add_denormal_error(dom, abs_err, rel_err)




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
