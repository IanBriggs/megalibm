#!/usr/bin/env python3


import matplotlib.pyplot as plt
import os.path as path
import sys


def plot_error(input_choice, x, fx, fpx, err):
    assert(x[0] == "Input")
    approx_fname = fpx[0]

    err[1:] = [abs(e) for e in err[1:]]
    
    # Filter out values when f(x) is near zero when doing relative error
    if err[0].startswith("abs_err_"):
        typ = "Absolute"
        assert(err[0] == "abs_err_{}".format(approx_fname))
    else:
        typ = "Relative"
        assert(err[0] == "rel_err_{}".format(approx_fname))
        

    title = "{} Error for {} input {}".format(typ, approx_fname, input_choice)

    # Plot of function
    fig, ax1 = plt.subplots()

    # Plot of error
    ax2 = ax1.twinx()

    # Labels
    ax1.set_title(title)
    ax1.set_xlabel("Input")
    ax1.set_ylabel("Output")
    ax2.set_ylabel("Error")

    # Zero error
    ax2.axhline(0, color="#FF00FF", linewidth=1)

    # 1/2 ULP from zero error
    if typ == "Relative":
        ax1.axhline(2**-53, color="#FF4500", linewidth=1)

    # y=0
    if any(i<=0.0 for i in x[1:]) and any(i>=0.0 for i in x[1:]):
        ax2.axvline(0, color="black", linewidth=1)

    # x=0
    if any(i<=0.0 for i in fx[1:]) and any(i>=0.0 for i in fx[1:]):
        ax2.axhline(0, color="black", linewidth=1)

    # Error
    ax1.scatter(x[1:], err[1:], s=1, color="red")

    # Oracle
    ax2.scatter(x[1:], fx[1:], s=1, color="blue", alpha=0.6)

    # Approximation
    ax2.scatter(x[1:], fpx[1:], s=2, color="purple", alpha=0.6)

    # Bigger image
    fig.set_size_inches(6.4*2, 4.8*2)

    fname = "{}.png".format(title.replace(" ", "_"))
    print('<img src="{}"/>'.format(fname))
    fig.savefig(fname)
    plt.close()

    maxabserr = max(err[1:])
    avgabserr = sum(err[1:])/len(err[1:])
    print("Avg value of error: {}".format(avgabserr))
    print("<hr>")

def plot_abs_vs_rel(input_choice, x, fx, fpx, abs_err, rel_err):
    assert(x[0] == "Input")
    approx_fname = fpx[0]        

    abs_err[1:] = [abs(d) for d in abs_err[1:]]
    rel_err[1:] = [abs(e) for e in rel_err[1:]]

    both_err = list(zip(abs_err[1:], rel_err[1:]))

    both_err.sort(key=lambda t:t[1])
    epsilon_eps_first = [t[1] for t in both_err[:-1]]
    abs_err_eps_first = [t[0] for t in both_err]
    delta_eps_first = list()
    cur = max(abs_err_eps_first)
    for i in range(len(both_err)-1):
        if abs_err_eps_first[i] == cur:
            cur = max(abs_err_eps_first[i+1:])
        delta_eps_first.append(cur)

    title = "Absolute vs Relative Error for {} input {}".format(approx_fname, input_choice)

    # Plot
    fig, ax1 = plt.subplots()

    # Labels
    ax1.set_title(title)
    ax1.set_xlabel("Relative Error")
    ax1.set_ylabel("Absolute Error")
    ax1.set_xscale("log")
    ax1.set_yscale("log")

    # abs vs rel error
    ax1.plot(epsilon_eps_first, delta_eps_first, color="blue")
    ax1.scatter(rel_err[1:], abs_err[1:], s=1, color="green")
    
    # rel_error = 1/2 ULP
    hulp = 2**-53
    if any(i<=hulp for i in rel_err[1:]) and any(i>=hulp for i in rel_err[1:]):
        ax1.axvline(hulp, color="#FF4500", linewidth=1)

    # abs_error = min finite
    mfin = 2**-1074
    if any(i<=mfin for i in abs_err[1:]) and any(i>=mfin for i in abs_err[1:]):
        ax1.axhline(mfin, color="#FF4500", linewidth=1)
        
    # Bigger image
    fig.set_size_inches(6.4*2, 4.8*2)

    fname = "{}.png".format(title.replace(" ", "_"))
    print('<img src="{}"/>'.format(fname))
    fig.savefig(fname)
    plt.close()



def read_dat(filename):
    print("Reading: {}".format(filename), flush=True)
    with open(filename, "r") as f:
        lines = f.readlines()
    print("  Parsing", flush=True)
    lines = [l.split() for l in lines]
    columns = [[lines[r][c] for r in range(len(lines))]
               for c in range(len(lines[0]))]
    columns = [[c[0]]+[float(i) for i in c[1:]] for c in columns]
    print("  Done", flush=True)
    return columns


def main(argv):
    fnames = argv[1:]
    columnss = [read_dat(fname) for fname in fnames]

    for columns,fname in zip(columnss, fnames):
        parts = fname.split("_")
        input_choice = parts[-1].split(".")[0]
        print("<header><h1>Plotting: {} (~correct rounding for whole expression)</h1></header>".format(columns[1][0]), flush=True)
        plot_error(input_choice, columns[0], columns[1], columns[1], columns[2])
        plot_error(input_choice, columns[0], columns[1], columns[1], columns[3])
        plot_abs_vs_rel(input_choice, columns[0], columns[1], columns[1], columns[2], columns[3])
        for i in range(4, len(columns), 3):
            print("<header><h1>Plotting: {}</h1></header>".format(columns[i][0]), flush=True)
            plot_error(input_choice, columns[0], columns[1], columns[i], columns[i+1])
            plot_error(input_choice, columns[0], columns[1], columns[i], columns[i+2])
            plot_abs_vs_rel(input_choice, columns[0], columns[1], columns[i], columns[i+1], columns[i+2])


if __name__ == "__main__":
    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
