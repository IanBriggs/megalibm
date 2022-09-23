#!/usr/bin/env python3

from copy import deepcopy
import datetime
from genericpath import isdir
import glob
import math
import json
import matplotlib.pyplot as plt
import os
import os.path as path
import sys


def double_list(l):
    ret = list()
    for a in l:
        ret.append(a)
        ret.append(a)
    return ret


def benchmark_to_webdata(dirname):
    # Return this:
    # ( <name>,
    #   <body>,
    #   { (<low>, <high>): # repeat for each json file
    #     { "regions": [<data...>],
    #       "data": { <impl_name>: # repeat for each impl
    #                 { <data_series_name>: [<data...>], # repeat for each data
    #                                                    #   series
    #                   "abs_metric": <abs_metric>,
    #                   "rel_metric": <rel_metric>,
    #                 }
    #               }
    #     }
    #   }
    # )
    name = None
    body = None
    benchmark_data = dict()
    json_files = glob.glob("{}/*.json".format(dirname))
    for file in sorted(json_files):
        with open(file, "r") as f:
            json_data = json.load(f)

        # check that names match
        if name is None:
            name = json_data["name"]
        assert name == json_data["name"]

        # check that bodies match
        if body is None:
            body = json_data["body"]
        assert body == json_data["body"]

        # get info for keys
        regions = json_data["regions"]
        low = min(regions)
        high = max(regions)

        # calculate average error of the correctly rounded implementation
        ref_data = json_data["functions"]["reference"]
        ref_avg_abs_err = (math.fsum(ref_data["abs_avg_errors"])
                           / len(ref_data["abs_avg_errors"]))
        ref_avg_rel_err = (math.fsum(ref_data["rel_avg_errors"])
                           / len(ref_data["rel_avg_errors"]))

        # calculate the metric and keep data series-es
        funcs_data = dict()
        for func in json_data["functions"]:
            func_data = deepcopy(json_data["functions"][func])
            func_avg_abs_err = (math.fsum(func_data["abs_avg_errors"])
                                / len(func_data["abs_avg_errors"]))
            func_avg_rel_err = (math.fsum(func_data["rel_avg_errors"])
                                / len(func_data["rel_avg_errors"]))
            abs_metric = func_avg_abs_err / ref_avg_abs_err
            rel_metric = func_avg_rel_err / ref_avg_rel_err
            func_data["abs_metric"] = abs_metric - 1.0
            func_data["rel_metric"] = rel_metric - 1.0
            funcs_data[func] = func_data

        # add this to the collection
        benchmark_data[(low, high)] = {
            "regions": regions,
            "data": funcs_data
        }

    return name, body, benchmark_data


def line_plot(title, input_regions, ref, libm, gens, domain_idx, log_y=False):
    """
    Generate an error plot.

    Keyword arguments:
    title -- Title of the plot
    input_regions -- sorted list of floats representing the domain
    ref -- list of floats representing error for the "real" function rounded to
           float
    libm -- list of floats representing error for the function implemented
            using libm
    gens -- list of lists of floats representing error for the
            megalibm-generated functions
    log_y -- boolean indicating whether the y-axis should be log scale
    """
    fig = plt.figure(facecolor=(1, 1, 1))
    ax1 = fig.add_subplot()

    # Setup our x values.
    # First and last are present once, all those in the middle are doubled.
    xs = list()
    xs.append(input_regions[0])
    for x in input_regions[1:-1]:
        xs.append(x)
        xs.append(x)
    xs.append(input_regions[-1])

    # Setup our data sets, all are doubled.
    ref_ys = double_list(ref)
    libm_ys = double_list(libm)
    gen_yss = list()
    for gen in gens:
        gen_yss.append(double_list(gen))

    # Line at y = 0
    ax1.axhline(0, color="black", linewidth=1)

    # Line at x = 0 if it is present in the graph
    if xs[0] <= 0.0 and xs[-1] >= 0.0:
        ax1.axvline(0, color="black", linewidth=1)

    # Plot all error sets
    ax1.plot(xs, ref_ys, label="correctly rounded", linewidth=2)
    ax1.plot(xs, libm_ys, label="libm")
    for i, gen_ys in enumerate(gen_yss):
        ax1.plot(xs, gen_ys, label="generated_{}".format(i))

    # Label the graph.
    ax1.set_title(title)
    ax1.set_xlabel("Input")
    if "Error" in title:
        ax1.set_ylabel("Error")
    else:
        ax1.set_ylabel("Value")
    ax1.legend()

    # optionally set log scale
    if log_y:
        ax1.set_yscale('log')

    # Bigger image
    fig.set_size_inches(6.4*2, 4.8*2)

    # Save and close
    outname = "{}_domain_{}.png".format(title.replace(" ", "_"), domain_idx)
    plt.savefig(outname, bbox_inches='tight')
    plt.close()

    return outname


def to_eps_del(abs_err, rel_err):
    """
    Turn the lists of absolute and relative errors into all pairs of epsilon
    and delta that can describe the error of the function.

    Keyword arguments:
    abs_err -- list of maximum absolute errors over contiguous regions
    rel_err -- list of maximum relative errors over the same regions
    """
    # Keep the pairing of absolute and relative error
    both = list(zip(rel_err, abs_err))

    # Sort so we get increasing absolute error with any ties sorted by
    # relative error
    both.sort(key=lambda t: t[0])
    both.sort(key=lambda t: t[1])

    # Delta errors are the absolute errors
    delt = [t[1] for t in both][:-1]

    # The corresponging epsilon will be the maximum of the relative errors to
    # the right of the same index
    rel_err = [t[0] for t in both]
    epsi = list()
    cur = max(rel_err[1:])
    for i in range(len(delt)):
        # The max will always be the same until we reach that maximum element
        if cur == rel_err[i]:
            cur = max(rel_err[i+1:])
        epsi.append(cur)
    return delt, epsi


def plot_abs_vs_rel(title, ref, libm, gens, domain_idx):
    """
    Generate an epsilon vs delta plot

    Keyword arguments:
    title -- Title of the plot
    ref -- list of pairs of floats representing absolute and relative error
           for the "real" function rounded to float
    libm -- list of pairs of floats representing absolute and relative error
            for the libm version of the function
    gens -- list of lists of pairs of floats representing  absolute and
            relative error for the megalibm-generated functions
    """
    fig = plt.figure(facecolor=(1, 1, 1))
    ax1 = fig.add_subplot()

    # Lines for x = 0 and y = 0
    ax1.axhline(0, color="black", linewidth=1)
    ax1.axvline(0, color="black", linewidth=1)

    # reference error
    ref_del, ref_eps = to_eps_del(*ref)
    ax1.plot(ref_del, ref_eps, marker="o",
             label="correcly rounded", linewidth=2)

    # libm error
    libm_del, libm_eps = to_eps_del(*libm)
    ax1.plot(libm_del, libm_eps, marker="o", label="libm")

    # generated function error
    for i, gen in enumerate(gens):
        gen_del, gen_eps = to_eps_del(*gen)
        ax1.plot(gen_del, gen_eps, marker="o", label="generated_{}".format(i))

    # Label the graph.
    ax1.set_title(title)
    ax1.set_xlabel("Absolute")
    ax1.set_ylabel("Relative")
    ax1.legend()

    # Use log scale for both axies
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # Bigger image
    fig.set_size_inches(6.4*2, 4.8*2)

    # Save and close
    outname = "{}_domain_{}.png".format(title.replace(" ", "_"), domain_idx)
    plt.savefig(outname, bbox_inches='tight')
    plt.close()

    return outname


def plot_region(name, regions, data, domain_idx):
    ref_data = data["reference"]

    possible_libm = [f for f in data if f.startswith("libm_")]
    assert len(possible_libm) == 1
    libm_name = possible_libm[0]
    libm_data = data[libm_name]

    gen_datas = [data[f] for f in data if f not in {"reference", libm_name}]

    imgnames = list()

    print("    Value")
    name = line_plot("{} Value".format(name),
                     regions,
                     ref_data["avg_value"],
                     libm_data["avg_value"],
                     [gen_data["avg_value"] for gen_data in gen_datas],
                     domain_idx)
    imgnames.append(name)

    print("    Absolute error")
    name = line_plot("{} Absolute Error".format(name),
                     regions,
                     ref_data["abs_max_errors"],
                     libm_data["abs_max_errors"],
                     [gen_data["abs_max_errors"] for gen_data in gen_datas],
                     domain_idx)
    imgnames.append(name)

    print("    Relative error")
    name = line_plot("{} Relative Error".format(name),
                     regions,
                     ref_data["rel_max_errors"],
                     libm_data["rel_max_errors"],
                     [gen_data["rel_max_errors"] for gen_data in gen_datas],
                     domain_idx)
    imgnames.append(name)

    print("    Epsilon vs Delta")
    name = plot_abs_vs_rel(
        "{} Epsilon vs Delta".format(name),
        (ref_data["abs_max_errors"], ref_data["rel_max_errors"]),
        (libm_data["abs_max_errors"], libm_data["rel_max_errors"]),
        [(gen_data["abs_max_errors"], gen_data["rel_max_errors"])
         for gen_data in gen_datas],
         domain_idx)
    imgnames.append(name)

    return imgnames


def plot_benchmark(name, benchmark_data, dirname):
    start = os.getcwd()
    os.chdir(dirname)

    img_data = dict()

    for domain_idx, (domain, things) in enumerate(benchmark_data.items()):
        print("  on domain [{}, {}]".format(domain[0], domain[1]))
        regions = things["regions"]
        data = things["data"]
        img_data[domain] = plot_region(name, regions, data, domain_idx)

    os.chdir(start)

    return img_data


def make_per_benchmark_webpage(name, body, img_data):
    today = datetime.date.today()
    y = today.year
    m = today.month
    d = today.day
    lines = [
        "<!doctype html>",
        "<html>",
        "<head>",
        "<title>{}: Megalibm Results for {}-{}-{}</title>".format(
            name, y, m, d),
        "<style>",
        ".func {",
        "font-size: 300%;",
        "}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>{}</h1>".format(name),
        "<div class=\"func\">{}</div>".format(body),
    ]

    for domain, imgs in img_data.items():
        lines.extend([
            "<h2> Domain [{}, {}]</h2>".format(domain[0], domain[1]),
            "<h3>Value</h3>",
            "<img src=\"{}\" style=\"width:50%\">".format(imgs[0]),
            "<h3>Absolute Error</h3>",
            "<img src=\"{}\" style=\"width:50%\">".format(imgs[1]),
            "<h3>Relative Error</h3>",
            "<img src=\"{}\" style=\"width:50%\">".format(imgs[2]),
            "<h3>Epsilon vs Delta</h3>",
            "<img src=\"{}\" style=\"width:50%\">".format(imgs[3]),
        ])

    lines.extend([
        "</body>",
        "</hmtl>"
    ])

    return "\n".join(lines)


def make_main_webpage(benchmarks_data):
    today = datetime.date.today()
    y = today.year
    m = today.month
    d = today.day
    lines = [
        "<!doctype html>",
        "<html>",
        " <head>",
        "  <title>Megalibm Results for {}-{}-{}</title>".format(y, m, d),
        " </head>",
        " <body>",
        "  <h1>General Metrics</h1>",
        "  <p>",
        "    Each benchmark has an oracle implementation made by a direct",
        "     translation of the benchmark into MPFR calls utilizing 512 bits",
        "     of precision.",
        "    This is the proxy for a real valued implementation and is used",
        "     for all reported error.",
        "    The correctly rounded implementation is simply rounding the",
        "     output of this oracle to double precision.",
        "    The libm version is a direct translation using the system libm,",
        "     currently 2.31-13+deb11u4. ",
        "    The other versions are generated by Megalibm.",
        "  </p>",
        "  <p>",
        "    Each domain is broken into 256 linear regions.",
        "    For each region 4096 random points are chosen and evaluated with",
        "     all implementations.",
        "    The metric reported here is the average error of these points",
        "     for an implementation divided by the average error for the",
        "     correctly rounded implementation minus one.",
        "    Therefore a metric of zero means correclty rounded.",
        "    This metric is calculated for both absolute and relative error.",
        "  </p>",
    ]

    for dirname, benchmark in benchmarks_data.items():
        name = benchmark[0]
        data = benchmark[2]
        lines.extend([
            "<h2><a href=\"{}/index.html\">{}</a></h2>".format(dirname, name),
            "  <table>",
            "    <tr>",
            "      <th>Implementation</th>",
        ])
        for domain in data:
            lines.append(
                "      <th align='right'>Domain </th><th align='left'>[{}, {}]</th>".format(domain[0], domain[1]))

        lines.extend([
            "    </tr>",
            "    <tr>",
            "      <th></th>",
            ])
        for domain in data:
            lines.append("      <th>abs</th><th>rel</th>")

        lines.append("    </tr>")

        for fname in data[domain]["data"]:
            if fname == "reference":
                continue
            lines.extend([
                "    <tr>",
                "      <td>{}</td>".format(fname),
            ])
            for domain in data:
                abs_metric = data[domain]["data"][fname]["abs_metric"]
                rel_metric = data[domain]["data"][fname]["rel_metric"]
                lines.append(
                    "      <td>{:0.4e}</td><td>{:0.4e}</td>".format(abs_metric, rel_metric))

            lines.append("    </tr>")

        lines.extend([
            "  </table>",
            "</body>",
            "</html>",
        ])

    return "\n".join(lines)


def main(argv):
    root = argv[1]

    benchmarks_data = dict()

    for bench_name in sorted(os.listdir(root)):
        dirname = path.join(root, bench_name)
        if not path.isdir(dirname):
            print("Skipping: '{}'".format(dirname))
            continue
        name, body, benchmark_data = benchmark_to_webdata(dirname)
        print("Plotting {}".format(dirname))
        img_data = plot_benchmark(name, benchmark_data, dirname)
        html = make_per_benchmark_webpage(name, body, img_data)
        with open(path.join(dirname, "index.html"), "w") as f:
            f.write(html)
        benchmarks_data[bench_name] = name, body, benchmark_data

    html = make_main_webpage(benchmarks_data)
    with open(path.join(root, "index.html"), "w") as f:
        f.write(html)


if __name__ == "__main__":
    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
