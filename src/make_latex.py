#!/usr/bin/env python3

import datetime
import os.path as path
import sys
import ast

import pandas as pd

BIN_DIR = path.abspath(path.dirname(__file__))
GIT_DIR = path.split(BIN_DIR)[0]
SRC_DIR = path.join(GIT_DIR, "src")
REQ_DIR = path.join(GIT_DIR, "requirements")
sys.path.append(SRC_DIR)

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os
import argparse
import json
from utils import Logger, Timer

logger = Logger(Logger.LOW, color=Logger.blue, def_color=Logger.cyan)
timer = Timer()

def format_float(number):
    # Check if the number is smaller than 1 and has an exponent
    if abs(number) < 1 and 'e' in str(number):
        # Format the number with 2 digits after the decimal and the correct exponent
        return "{:.2e}".format(number)
    elif abs(number) > 100:
        # Format large numbers in scientific notation
        return "{:.2e}".format(number)
    else:
        # Format the number with 2 digits after the decimal
        return "{:.2f}".format(number)

def make_benchmark_page(benchmark_data, benchmark_body,
                         abs_err_images, benchmark_name):
    #TODO GET NAME AND BODY
    # benchmark_name = benchmark_data["func_name"]
    today = datetime.date.today()
    y = today.year
    m = today.month
    d = today.day
    parts = [f"""
    <!doctype html>
    <meta charset="UTF-8">
    <html>

    <head>
        <title>{benchmark_name} Results for {y}-{m}-{d}</title>
        <link rel="stylesheet" href="../../style.css">
    </head>

    <body>
        <div class="rounded-box top-box">
            <h1 class="main-title">{benchmark_name}</h1>
            <div class="fpcore">
                {benchmark_body}
            </div>
        </div>
    """.replace("\n    ", "\n").strip()]

    for idx, domain_name in enumerate(sorted(benchmark_data.keys())):
        abs = abs_err_images[domain_name]
        parts.append(f"""
        <div class="rounded-box result-box">
            <h2 class="result-title">Domain {idx}: {domain_name}</h2>
            <div class="result-quad">
                <div class="row">
                    <div class="plot">
                        <img class="plot-image" src="{abs}">
                    </div>
                </div>
            </div>
        </div>
        """.replace("\n    ", "\n").rstrip())

    parts.append("""
    </body>

    </html>
    """.replace("\n    ", "\n").strip())

    return "\n".join(parts)


def make_func_rows(funcs, lib, accumulator):
    for idx, func in enumerate(funcs):
        func_data = funcs[func]
        i = 0
        for dom, row in func_data.items():
            # x = list(map(lambda x: format_float(x),ast.literal_eval(dom)))
            # y = str(x)

            # domain = ", ".join(list(map(lambda x: format_float(x), dom.strip("[]").split(","))))
            # dom_out = f"[{domain}]"
            err_mlm = format_float(float(row['MLM error']))
            err_lib = format_float(float(row['Reference error']))
            time_mlm = format_float(float(row['MLM time']))
            time_lib = format_float(float(row['Reference time']))
            is_err_mlm_better = float(err_mlm) <= float(err_lib)
            is_time_mlm_better = float(time_mlm) <= float(time_lib)
            text_mlm_err = r"\textbf{" + f"{err_mlm}" + r"}" if is_err_mlm_better else f"{err_mlm}"
            text_mlm_time =  r"\textbf{" + f"{time_mlm}" + r"}" if is_time_mlm_better else f"{time_mlm}"
            text_lib_err = r"\textbf{" + f"{err_lib}" + r"}" if not is_err_mlm_better else f"{err_lib}"
            text_lib_time = r"\textbf{" + f"{time_lib}" + r"}" if not is_time_mlm_better else f"{time_lib}"
            table_row = []
            table_row.append(f" {lib if i == 0 else ''}")
            table_row.append(f" {func if i == 0 else ''}")
            table_row.append(f" {dom}")
            table_row.append(f" {text_mlm_err}")
            table_row.append(f" {text_lib_err}")
            table_row.append(f" {text_mlm_time}")
            table_row.append(f" {text_lib_time}")
            accumulator.append("&".join(table_row) + "\\\\")
            i += 1
    accumulator.append("    \hline")





def make_latex_table_rows(data):
    lines = []
    for lib in data.keys():
        funcs_data = data[lib]
        make_func_rows(funcs_data, lib, lines)

    return "\n".join(lines)


def make_latex_table(data):
    table_head = r"\begin{tabular}{|l|l|l|l|l|l|l|} \hline"
    table_cols = r"Lib & Func & Domain & Error MLM & Error Libm & Runtime MLM & Runtime libm \\ \hline"
    table_end = r"\end{tabular}"
    return f"""
    {table_head}
    {table_cols}
    {make_latex_table_rows(data)}
    {table_end}
    """.replace("\n    ", "\n").strip()



   
def make_table_rows(table_data):
    lines = []
    for dom, row in table_data.items():
        lines.append("              <tr>")
        lines.append(f"                 <th>{dom}</th>")
        lines.append(f"                 <td>{format_float(row['MLM time'])}</td>")
        lines.append(f"                 <td>{format_float(row['Reference time'])}</td>")
        lines.append(f"                 <td>{format_float(row['MLM error'])}</td>")
        lines.append(f"                 <td>{format_float(row['Reference error'])}</td>")
        lines.append("              </tr>")
    return "\n".join(lines)


def make_main_part(generation_dir, benchmark_name, table_data):
    dir = generation_dir
    name = benchmark_name

    return f"""
    <div class="rounded-box result-box">
        <h2 class="result-title">
            <a href="{dir}/{name}/index.html">{name}</a>
        </h2>
        <div class="table">
            <table class="dataframe">
                <thead>
                    <tr style="text-align: right;">
                    <th>Domain</th>
                    <th>MLM time</th>
                    <th>Reference time</th>
                    <th>MLM error</th>
                    <th>Reference error</th>
                    </tr>
                </thead>
                <tbody>
                {make_table_rows(table_data)}
                </tbody>
            </table>
        </div>
    </div>
    """.rstrip()

def make_main_page(generation_dir, benchmark_names, benchmarks_datas):
    today = datetime.date.today()
    y = today.year
    m = today.month
    d = today.day

    parts = [f"""
    <!doctype html>
    <meta charset="UTF-8">
    <html>

    <head>
        <title>Main Megalibm Results for {y}-{m}-{d}</title>
        <link rel="stylesheet" href="style.css">
    </head>

    <body>
        <div class="rounded-box top-box">
            <h1 class="main-title">General Metrics</h1>
            <p class="description">
                Each benchmark has 4 different domains that we examine for
                both error and speed.

                For each of these we create a plot shown here providing an
                overview of generated functions as well as the default libm
                on the system.

                These plots show error and speed normalized such that the
                system libm is [1,1].

                Error is on the X axis, with further to the left being
                higher error.

                Specifically, this is the maximum relative error found from
                sampling thea domain.

                Speedup is on the Y axis, with further up being faster code.

                All points are plotted, but the pareto front is plotted as
                a stepped line.
            </p>
            <h2 class="subtitle">TL:DR</h2>
            <p class="description">
            <ul class="description">
                <li>up and right are better</li>
                <li>blue dot is libm</li>
                <li>orange dots are generated</li>
                <li>line shows best generated</li>
            </ul>
            </p>
        </div>
    """.replace("\n    ", "\n").strip()]

    for bench_name in benchmark_names:
        parts.append(make_main_part(generation_dir,
                     bench_name, benchmarks_datas[bench_name]["table_data"].to_dict()))

    parts.append("""
    </body>

    </html>
    """.replace("\n    ", "\n").strip())

    text = "\n".join(parts)

    return text



def make_css():
    return """
    * {
    font-family: 'Courier New', Courier, monospace;
    margin: auto;
    width: auto;
    }
    body {
        /* background-color: #232b2b; */
        background-color: #006699;
        max-width: 1200px;
    }
    .rounded-box {
        border-radius: 20px;
        padding: 5px;
        margin-top: 5px;
        border-width: 5px;
        border-style: solid;
        border-color: #003b6f;
        background-color: #acacac;
    }
    .description {
        font-weight: bold;
    }
    ul.description {
        padding-left: 15px;
    }
    .summary {
        font-weight: bold;
        font-size: 200%
    }
    .subtitle {
        margin-top: 20px;
    }
    .result-box {
        padding-bottom: 0;
    }
    .result-quad {
        display: flex;
        flex-direction: column;
    }
    .result-title {
        margin-bottom: 10px;
    }
    .row {
        display: flex;
        flex-direction: row;
        width: 100%;
        gap: 5px;
    }
    .plot {
        width: 100%;
        position: relative;
        text-align: center;
    }
    .emoji-indicator {
        position: absolute;
        top: -2%;
        left: 0;
        font-size: 300%;
    }
    .plot-image {
        width: 100%;
        border-radius: 10px;
    }
    pre {
        font-size: 200%;
        white-space: pre-wrap;
    }
    ul.legend {
        list-style: none;
        padding-left: 1.375em;
        margin-left: 0.25em;
        margin-bottom: 1em;
    }
    li.legend {
        position: relative;
        font-weight: bold;
    }
    span.legend {
        position: relative;
    }
    .legend-color {
        position: absolute;
        left: -1.375em;
        width: 1em;
        height: 1em;
        border-style: solid;
        border-width: 2px;
    }
    table.dataframe {
    border-collapse: collapse;
    width: 100%;
    padding: 10px; 
    /* border-radius: 20px; */
    /* display: flex; */
    /* flex-direction: column; */
    }

    table.dataframe th,
    table.dataframe td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }

    table.dataframe th,
    table.dataframe td {
        background-color: #f2f2f2;
    }
    """.replace("\n    ", "\n").strip()


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        description='Generate the website for nightly runs')
    parser.add_argument("-v", "--verbosity",
                        nargs="?",
                        default="medium",
                        const="medium",
                        choices=list(Logger.CONSTANT_DICT),
                        help="Set output verbosity")
    parser.add_argument("-l", "--log-file",
                        nargs="?",
                        type=str,
                        help="Redirect logging to given file.")
    parser.add_argument("dirname",
                        help="Directory with the generated functions and data")
    args = parser.parse_args(argv[1:])

    Logger.set_log_level(Logger.str_to_level(args.verbosity))

    if args.log_file is not None:
        Logger.set_log_filename(args.log_file)

    logger.dlog("Settings:")
    logger.dlog("    dirname: {}", args.dirname)
    logger.dlog("  verbosity: {}", args.verbosity)
    logger.dlog("   log-file: {}", args.log_file)

    return args

def read_data(dirname):
    logger("Reading from directory: {}", dirname)
    benchmark_data = dict()
    fname = path.join(dirname, "data.json")

    benchmark_df = pd.read_json(fname)
    return benchmark_df

def main(argv):
    args = parse_arguments(argv)

    base = path.abspath(args.dirname)

    print("DIRNAME", args.dirname)

    benchmark_names = list()
    latex_table_data = dict()
    benchmarks_datas = dict()



    # Look through directory contents
    for name in sorted(os.listdir(base)):
        os.chdir(base)

        # Skip non-directories
        if not path.isdir(name):
            logger.warning("Skipping: {}", name)
            continue

        # Read data for the benchmark
        benchmark_data = read_data(name)
        
        # Setup collections
        benchmark_names.append(name)
        benchmarks_datas[name] = benchmark_data

        #Plot Images
        abs_err_images = dict()
        for idx, dom in enumerate(sorted(benchmark_data["table_data"].to_dict().keys())):
            func_name = benchmark_data["func_name"].iloc[0]
            fname = f"{func_name}_domain_{idx}_absolute_error_abs_max_errors.png"
            abs_err_images[dom] = fname

        # Collect latex table data
        splitted_name = name.split("_")
        library = splitted_name[1]
        version = "_".join(splitted_name[2:])
        if library not in latex_table_data:
            latex_table_data[library] = dict()
        latex_table_data[library][version] = benchmark_data["table_data"].to_dict()

        func_body = benchmark_data["func_body"].iloc[0]
        html = make_benchmark_page(benchmark_data["table_data"].to_dict(), func_body,
                                   abs_err_images, name)
        logger("Writing benchmark webpage: {}", name)
        with open(f"{name}/index.html", "w") as f:
            f.write(html)

    # Make webpages
    gen_dir = path.split(base)[1]
    html = make_main_page(gen_dir ,benchmark_names, benchmarks_datas)
    logger("Writing main index.html")
    logger("Writing main .tex")
    os.chdir(base)
    os.chdir("..")

    latex_table = make_latex_table(latex_table_data)
    # TODO: split table parts
    with open("table.tex", "w") as f:
        f.write(latex_table)

    with open("index.html", "w") as f:
        f.write(html)
    css = make_css()
    with open("style.css", "w") as f:
        f.write(css)


if __name__ == "__main__":
    return_code = 0
    try:
        ar = ["py", "/Users/yashlad/workspace/megalibm/nightlies/1688763981/generated"]
        # return_code = main(sys.argv)
        return_code = main(ar)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(return_code)
