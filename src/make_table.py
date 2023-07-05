#!/usr/bin/env python3

import datetime
import os.path as path
import sys

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

emoji_meter = [
    '\N{disappointed face}',
    '\N{slightly smiling face}',
    '\N{grinning face}',
    '\N{confused face}',
]

# Main result
libm_color = "#006699"
generated_color = "#FC4C02"

# Per benchmark plots
reference_color = "xkcd:vivid green"
color_cycle = [
    "xkcd:purple",
    "xkcd:pink",
    "xkcd:brown",
    "xkcd:red",
    "xkcd:light blue",
    "xkcd:teal",
    "xkcd:orange",
    "xkcd:light green",
    "xkcd:magenta",
    "xkcd:yellow",
    "xkcd:sky blue",
    "xkcd:grey",
    "xkcd:lime green",
    "xkcd:light purple",
    "xkcd:violet",
    "xkcd:dark green",
    "xkcd:turquoise",
    "xkcd:lavender",
    "xkcd:dark blue",
    "xkcd:tan",
    "xkcd:cyan",
    "xkcd:aqua",
    "xkcd:forest green",
    "xkcd:mauve",
    "xkcd:dark purple",
    "xkcd:bright green",
    "xkcd:maroon",
    "xkcd:olive",
    "xkcd:salmon",
    "xkcd:beige",
    "xkcd:royal blue",
    "xkcd:navy blue",
    "xkcd:lilac",
    "xkcd:black",
    "xkcd:hot pink",
    "xkcd:light brown",
    "xkcd:pale green",
    "xkcd:peach",
    "xkcd:olive green",
    "xkcd:dark pink",
    "xkcd:periwinkle",
    "xkcd:sea green",
    "xkcd:lime",
    "xkcd:indigo",
    "xkcd:mustard",
    "xkcd:light pink",
]


def determine_emoji(gen_speedup_s, gen_errup_s):
    # libm beat us for everything
    if (all(s < 1.0 for s in gen_speedup_s)
            and all(a > 1.0 for a in gen_errup_s)):
        return emoji_meter[0]

    # We have some batter points, but libm is still above the pareto front
    pareto_xs, pareto_ys = pareto_front_points(gen_errup_s + [1.0],
                                               gen_speedup_s + [1.0])
    if (1.0, 1.0) in zip(pareto_xs, pareto_ys):
        return emoji_meter[1]

    # We beat libm
    return emoji_meter[2]


def domain_name(data):
    low = data["error"]["regions"][0]
    high = data["error"]["regions"][-1]
    return f"[{low}, {high}]"


def double_list(l):
    ret = list()
    for a in l:
        ret.append(a)
        ret.append(a)
    return ret


def pareto_front_points(xs, ys):
    points = list(zip(xs, ys))
    points.sort(key=lambda p: p[0])

    pareto_points = [points[0]]
    for p in points:
        if p[1] > pareto_points[-1][1]:
            pareto_points.append(p)

    return [p[0] for p in pareto_points], [p[1] for p in pareto_points]


def abs_rel_to_del_eps(abs_err, rel_err):
    # Keep the pairing of absolute and relative error
    both = list(zip(rel_err, abs_err))

    # Sort so we get increasing absolute error with any ties sorted by
    # relative error
    both.sort(key=lambda t: t[0])
    both.sort(key=lambda t: t[1])

    # Delta errors are the absolute errors
    deltas = [t[1] for t in both][:-1]

    # The corresponding epsilon will be the maximum of the relative errors to
    # the right of the same index
    rel_err = [t[0] for t in both]
    epsilons = list()
    cur = max(rel_err[1:])
    for i in range(len(deltas)):
        # The max will always be the same until we reach that maximum element
        if cur == rel_err[i]:
            cur = max(rel_err[i + 1:])
        epsilons.append(cur)
    return deltas, epsilons

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


def format_float(number):
    # Check if the number is smaller than 1 and has an exponent
    if abs(number) < 1 and 'e' in str(number):
        # Format the number with 2 digits after the decimal and the correct exponent
        return "{:.2e}".format(number)
    else:
        # Format the number with 2 digits after the decimal
        return "{:.2f}".format(number)
    
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


def read_data(dirname):
    logger("Reading from directory: {}", dirname)
    benchmark_data = dict()
    fname = path.join(dirname, "data.json")

    benchmark_df = pd.read_json(fname)
    return benchmark_df


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


def main(argv):
    args = parse_arguments(argv)

    base = path.abspath(args.dirname)

    print("DIRNAME", args.dirname)

    benchmark_names = list()
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

        print("BENECHMARK_DATA", type(benchmark_data))
        print("BENECHMARK_DATA", benchmark_data["table_data"].to_dict())

        # Setup collections
        benchmark_names.append(name)
        benchmarks_datas[name] = benchmark_data


        abs_err_images = dict()

        # os.chdir(name)

        # Plot images
        for idx, dom in enumerate(sorted(benchmark_data["table_data"].to_dict().keys())):
            func_name = benchmark_data["func_name"].iloc[0]
            # print("bench_col!!!!", benchmark_data["func_name"], type(benchmark_data["func_name"]))
            # print("corr_!!!!", benchmark_data["func_name"].iloc[0], type(benchmark_data["func_name"].iloc[0]))
            # print("func_name!!!!", func_name, type(func_name))
            fname = f"{func_name}_domain_{idx}_absolute_error_abs_max_errors.png"
            abs_err_images[dom] = fname
        # Output benchmark webpage
        # func_body = "LAMBDA"
        func_body = benchmark_data["func_body"].iloc[0]
        html = make_benchmark_page(benchmark_data["table_data"].to_dict(), func_body,
                                   abs_err_images, name)
        logger("Writing benchmark webpage: {}", name)
        with open(f"{name}/index.html", "w") as f:
            f.write(html)

    # Make webpages
    gen_dir = path.split(base)[1]
    html = make_main_page(gen_dir, benchmark_names, benchmarks_datas)
    logger("Writing main index.html")
    os.chdir(base)
    os.chdir("..")
    with open("index.html", "w") as f:
        f.write(html)
    css = make_css()
    with open("style.css", "w") as f:
        f.write(css)


if __name__ == "__main__":
    return_code = 0
    try:
        return_code = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(return_code)
