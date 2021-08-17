#!/usr/bin/env python3


import json
import matplotlib.pyplot as plt
import os.path as path
import sys


def plot_error(title, input_regions, error0, error1, log_y=False):
    fig = plt.figure(facecolor=(1, 1, 1))
    ax1 = fig.add_subplot()

    xs = list()
    xs.append(input_regions[0])
    for x in input_regions[1:-1]:
        xs.append(x)
        xs.append(x)
    xs.append(input_regions[-1])

    y0s = list()
    y1s = list()
    for y0, y1 in zip(error0, error1):
        y0s.append(y0)
        y0s.append(y0)
        y1s.append(y1)
        y1s.append(y1)


    #ax1.set_title(title)
    ax1.set_xlabel("Input")
    ax1.set_ylabel("Error")
    
    # x = 0
    ax1.axhline(0, color="black", linewidth=1)
    
    # y = 0
    if any(i<=0.0 for i in xs) and any(i>=0.0 for i in xs):
        ax1.axvline(0, color="black", linewidth=1)
    
    # error
    ax1.plot(xs, y0s, label="libm")
    ax1.plot(xs, y1s, label="generated")
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


def plot_abs_vs_rel(title, abs0, rel0, abs1, rel1):
    fig = plt.figure(facecolor=(1, 1, 1))
    ax1 = fig.add_subplot()

    #ax1.set_title(title)
    ax1.set_xlabel("Absolute")
    ax1.set_ylabel("Relative")
    
    # x = 0
    ax1.axhline(0, color="black", linewidth=1)
    ax1.axvline(0, color="black", linewidth=1)
    
    # error
    del0, eps0 = to_eps_del(abs0, rel0)
    del1, eps1 = to_eps_del(abs1, rel1)
    ax1.plot(del0, eps0, marker="o", label="libm")
    ax1.plot(del1, eps1, marker="o", label="generated")
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

        print("  Plotting 1/3")
        plot_error("Absolute Error Domain {}".format(input_typ),
                   data["regions"], 
                   data["functions"]["libm_versin"]["abs_max_errors"],
                   data["functions"]["my_versin_26"]["abs_max_errors"])
        print("  Plotting 2/3")
        plot_error("Relative Error Domain {}".format(input_typ),
                   data["regions"], 
                   data["functions"]["libm_versin"]["rel_max_errors"],
                   data["functions"]["my_versin_26"]["rel_max_errors"],
                   True)
        print("  Plotting 3/3")
        plot_abs_vs_rel("Absolute vs Relative Error Domain {}".format(input_typ),
                        data["functions"]["libm_versin"]["abs_max_errors"],
                        data["functions"]["libm_versin"]["rel_max_errors"],
                        data["functions"]["my_versin_26"]["abs_max_errors"],
                        data["functions"]["my_versin_26"]["rel_max_errors"])
        print("  Done")


if __name__ == "__main__":
    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
