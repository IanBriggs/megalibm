#!/usr/bin/env python3


import json
import matplotlib.pyplot as plt
import os.path as path
import sys

def double_list(l):
    ret = list()
    for a in l:
        ret.append(a)
        ret.append(a)
    return ret

def plot_error(title, input_regions, ref, libm, gens, log_y=False):
    fig = plt.figure(facecolor=(1, 1, 1))
    ax1 = fig.add_subplot()

    xs = list()
    xs.append(input_regions[0])
    for x in input_regions[1:-1]:
        xs.append(x)
        xs.append(x)
    xs.append(input_regions[-1])

    ref_ys = double_list(ref)
    libm_ys = double_list(libm)
    gen_yss = list()
    for gen in gens:
        gen_yss.append(double_list(gen))

    #ax1.set_title(title)
    ax1.set_xlabel("Input")
    ax1.set_ylabel("Error")

    # x = 0
    ax1.axhline(0, color="black", linewidth=1)

    # y = 0
    if any(i<=0.0 for i in xs) and any(i>=0.0 for i in xs):
        ax1.axvline(0, color="black", linewidth=1)

    # error
    ax1.plot(xs, ref_ys, label="correctly rounded")
    ax1.plot(xs, libm_ys, label="libm")
    for i,gen_ys in enumerate(gen_yss):
        ax1.plot(xs, gen_ys, label="generated_{}".format(i))
    
    ax1.legend()

    # optionally set log scale
    if log_y:
        ax1.set_yscale('log')

    # Bigger image
    fig.set_size_inches(6.4*2, 4.8*2)

    plt.savefig("{}.png".format(title.replace(" ", "_")), bbox_inches='tight')

    plt.close()


def to_eps_del(abs_err, rel_err):
    both = list(zip(rel_err, abs_err))
    both.sort(key=lambda t:t[1])
    delt = [t[1] for t in both][:-1]
    rel_err = [t[0] for t in both]
    epsi = list()
    cur = max(rel_err[1:])
    for i in range(len(delt)):
        if cur == rel_err[i]:
            cur = max(rel_err[i+1:])
        epsi.append(cur)
    return delt, epsi


def plot_abs_vs_rel(title, ref, libm, gens):
    fig = plt.figure(facecolor=(1, 1, 1))
    ax1 = fig.add_subplot()

    #ax1.set_title(title)
    ax1.set_xlabel("Absolute")
    ax1.set_ylabel("Relative")

    # x = 0
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

    # we want a legend
    ax1.legend()

    # set log scale
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # Bigger image
    fig.set_size_inches(6.4*2, 4.8*2)

    plt.savefig("{}.png".format(title.replace(" ", "_")), bbox_inches='tight')

    plt.close()


def main(argv):
    fnames = argv[1:]

    for fname in fnames:
        print("Reading {}".format(fname))
        in_dir = path.split(fname)[0]
        parts = fname.split("_")
        input_typ = parts[-1].split(".")[0]

        with open(fname, "r") as f:
            data = json.load(f)

        funcnames = data["functions"]

        ref_data = data["functions"]["reference"]
        
        libm_name = [f for f in funcnames if "libm" in f][0]
        libm_data = data["functions"][libm_name]
        
        gen_datas = [data["functions"][n] for n in funcnames 
                     if n != "reference" 
                     and n != libm_name]
        
        print("  Plotting 1/3")
        plot_error("Absolute Error Domain {}".format(input_typ),
                   data["regions"],
                   ref_data["abs_max_errors"],
                   libm_data["abs_max_errors"],
                   [gen_data["abs_max_errors"] for gen_data in gen_datas])
        print("  Plotting 2/3")
        plot_error("Relative Error Domain {}".format(input_typ),
                   data["regions"],
                   ref_data["rel_max_errors"],
                   libm_data["rel_max_errors"],
                   [gen_data["rel_max_errors"] for gen_data in gen_datas],
                   True)
        print("  Plotting 3/3")
        plot_abs_vs_rel("Absolute vs Relative Error Domain {}".format(input_typ),
                        (ref_data["abs_max_errors"], ref_data["rel_max_errors"]),
                        (libm_data["abs_max_errors"], libm_data["rel_max_errors"]),
                        [(gen_data["abs_max_errors"], gen_data["rel_max_errors"])
                         for gen_data in gen_datas])
        print("  Done")


if __name__ == "__main__":
    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
