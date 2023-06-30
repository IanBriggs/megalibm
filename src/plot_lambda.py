
import matplotlib.pyplot as plt
from error_function import error_function
from interval import Interval
import lambdas


def plot_lambda(domain: Interval,
                lambda_expression,
                name: str = None,
                samples: int = 2**17):
    lambda_expression.type_check()
    lambda_function_name = "lambda"
    _, lines = lambdas.generate_c_code(lambda_expression,
                                       lambda_function_name)
    lambda_code = "\n".join(lines)
    oracle_impl_type = lambda_expression.out_type
    precision = lambda_expression.numeric_type
    oracle_function_name = "oracle"
    _, lines = lambdas.generate_mpfr_c_code(oracle_impl_type,
                                            oracle_function_name,
                                            numeric_type=precision)
    oracle_code = "\n".join(lines)

    data = error_function(numeric_type=precision,
                          samples=samples,
                          c_function_name=lambda_function_name,
                          c_code=lambda_code,
                          oracle_function_name=oracle_function_name,
                          oracle_code=oracle_code,
                          domain=domain)

    data["max_cr_abs_error"] = data["cr_abs_error"].rolling(
        window=samples // 512).max()

    _, axes = plt.subplots(nrows=1, ncols=1, figsize=(5, 4))

    data.plot.scatter(x="input", y="f_abs_error", s=2**-4, ax=axes)
    data.plot.line(x="input", y="max_cr_abs_error", color="black",
                   linewidth=2, legend=False, ax=axes)
    axes.set_xlabel("Input")
    axes.set_ylabel("Error")

    if name is not None:
        axes.set_title(f"Absolute error for {name}")
    else:
        axes.set_title(f"Absolute error")

    y_min = 0
    y_max = max(data["f_abs_error"])
    axes.set_ylim(y_min, y_max)

    plt.tight_layout()

    return axes
