#!/usr/bin/env python3


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


def plot_error(title, input_regions, ref, libm, gens, log_y=False):
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
    ax1.plot(xs, ref_ys, label="correctly rounded")
    ax1.plot(xs, libm_ys, label="libm")
    for i, gen_ys in enumerate(gen_yss):
        ax1.plot(xs, gen_ys, label="generated_{}".format(i))

    # Label the graph.
    ax1.set_title(title)
    ax1.set_xlabel("Input")
    ax1.set_ylabel("Error")
    ax1.legend()

    # optionally set log scale
    if log_y:
        ax1.set_yscale('log')

    # Bigger image
    fig.set_size_inches(6.4*2, 4.8*2)

    # Save and close
    plt.savefig("{}.png".format(title.replace(" ", "_")), bbox_inches='tight')
    plt.close()


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


def plot_abs_vs_rel(title, ref, libm, gens):
    """
    Generate an epsilon vs delta plot

    Keyword arguments:
    title -- Title of the plot
    ref -- list of pairs of floats representing absolute and relative error for 
           the "real" function rounded to float
    libm -- list of pairs of floats representing absolute and relative error for
            the libm version of the function
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
    ax1.plot(ref_del, ref_eps, marker="o", label="correcly rounded")

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
    plt.savefig("{}.png".format(title.replace(" ", "_")), bbox_inches='tight')
    plt.close()


def triple_plot(filename):
    """
    Generate absolute, relative, and epsilon-vs-delta plots.

    Keyword arguments:
    filename -- A json file with the following structure:

    {
        "regions": [],
        "functions": {
            "reference": {
                "abs_max_errors": [],
                "abs_avg_errors": [],
                "abs_med_errors": [],
                "rel_max_errors": [],
                "rel_avg_errors": [],
                "rel_med_errors": []
            },
            "libm_<name>": { <errors lists> },
            <more function to errors>
        }
    }
    """
    print("Reading {}".format(filename))
    dirname, fname = path.split(filename)
    start = os.getcwd()
    os.chdir(dirname)

    with open(fname, "r") as f:
        data = json.load(f)

    ref_data = data["functions"]["reference"]

    possible_libm = [f for f in data["functions"] if f.startswith("libm_")]
    assert len(possible_libm) == 1
    libm_name = possible_libm[0]
    libm_data = data["functions"][libm_name]

    gen_datas = [data["functions"][f] for f in data["functions"]
                 if f not in {"reference", libm_name}]

    func_name = libm_name[len("libm_"):]

    basename = path.split(filename)[1]
    region_name = basename[basename.rindex("_"):basename.rindex(".")]
    if len(region_name) == 0:
        region_name = "UnknownRegion"

    print("  Plotting Absolute error")
    plot_error("{} Absolute Error Domain {}".format(func_name, region_name),
               data["regions"],
               ref_data["abs_max_errors"],
               libm_data["abs_max_errors"],
               [gen_data["abs_max_errors"] for gen_data in gen_datas])

    print("  Plotting Relative error")
    plot_error("{} Relative Error Domain {}".format(func_name, region_name),
               data["regions"],
               ref_data["rel_max_errors"],
               libm_data["rel_max_errors"],
               [gen_data["rel_max_errors"] for gen_data in gen_datas])

    print("  Plotting Epsilon vs Delta")
    plot_abs_vs_rel("{} Absolute vs Relative Error Domain {}".format(func_name, region_name),
                    (ref_data["abs_max_errors"],
                     ref_data["rel_max_errors"]),
                    (libm_data["abs_max_errors"],
                     libm_data["rel_max_errors"]),
                    [(gen_data["abs_max_errors"], gen_data["rel_max_errors"])
                     for gen_data in gen_datas])

    
    os.chdir(start)

def main(argv):
    fnames = argv[1:]

    for fname in fnames:
        triple_plot(fname)


if __name__ == "__main__":
    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
