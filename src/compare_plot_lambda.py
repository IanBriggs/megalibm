
import matplotlib.pyplot as plt
from error_function import error_function
from interval import Interval
import lambdas


def compare_plot_lambda(domain: Interval,
                        left_expression,
                        right_expression,
                        left_name: str = None,
                        right_name: str = None,
                        samples: int = 2**17):
    left_expression.type_check()
    left_function_name = "left"
    _, left_lines = lambdas.generate_c_code(left_expression,
                                            left_function_name)
    left_code = "\n".join(left_lines)

    right_expression.type_check()
    right_function_name = "right"
    _, right_lines = lambdas.generate_c_code(right_expression,
                                             right_function_name)
    right_code = "\n".join(right_lines)

    oracle_impl_type = left_expression.out_type
    precision = left_expression.numeric_type
    oracle_function_name = "oracle"
    _, left_lines = lambdas.generate_mpfr_c_code(oracle_impl_type,
                                                 oracle_function_name,
                                                 numeric_type=precision)
    oracle_code = "\n".join(left_lines)

    left_data = error_function(numeric_type=precision,
                               samples=samples,
                               c_function_name=left_function_name,
                               c_code=left_code,
                               oracle_function_name=oracle_function_name,
                               oracle_code=oracle_code,
                               domain=domain)

    right_data = error_function(numeric_type=precision,
                                samples=samples,
                                c_function_name=right_function_name,
                                c_code=right_code,
                                oracle_function_name=oracle_function_name,
                                oracle_code=oracle_code,
                                domain=domain)

    left_data["max_cr_abs_error"] = left_data["cr_abs_error"].rolling(
        window=samples//512).max()
    right_data["max_cr_abs_error"] = left_data["max_cr_abs_error"]

    y_min = 0
    y_max = max(max(left_data["f_abs_error"]), max(right_data["f_abs_error"]))

    _, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

    left_data.plot.scatter(x="input", y="f_abs_error", s=2**-4, ax=axes[0])
    left_data.plot.line(x="input", y="max_cr_abs_error", color="black",
                        linewidth=2, legend=False, ax=axes[0])

    right_data.plot.scatter(x="input", y="f_abs_error", s=2**-4, ax=axes[1])
    right_data.plot.line(x="input", y="max_cr_abs_error", color="black",
                         linewidth=2, legend=False, ax=axes[1])

    if left_name is not None:
        axes[0].set_title(f"Absolute error for {left_name}")
    else:
        axes[0].set_title(f"Absolute error")

    if right_name is not None:
        axes[1].set_title(f"Absolute error for {right_name}")
    else:
        axes[1].set_title(f"Absolute error")

    axes[0].set_xlabel("Input")
    axes[1].set_xlabel("Input")
    axes[0].set_ylabel("Error")
    axes[1].set_ylabel("Error")

    axes[0].set_ylim(y_min, y_max)
    axes[1].set_ylim(y_min, y_max)

    plt.tight_layout()

    return axes
