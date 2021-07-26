#!/usr/bin/env python3


import matplotlib.pyplot as plt
import os.path as path
import sys




def filter_subnormal(x, fx, fpx, err):
    nx = [x[0]]
    nfx = [fx[0]]
    nfpx = [fpx[0]]
    nerr = [err[0]]
    for i in range(1, len(x)):
        if abs(fx[i]) <= 2.225073858507201e-308:
            continue
        nx.append(x[i])
        nfx.append(fx[i])
        nfpx.append(fpx[i])
        nerr.append(err[i])

    return nx, nfx, nfpx, nerr


def plot_error(in_dir, input_typ, x, fx, fpx, err, abs_err=True):
    assert(x[0] == "Input")
    approx_fname = fpx[0]

    # Filter out values when f(x) is near zero when doing relative error
    if abs_err == True:
        typ = "Absolute"
        assert(err[0] == "abs_err_{}".format(approx_fname))
    else:
        typ = "Relative"
        assert(err[0] == "rel_err_{}".format(approx_fname))
        x, fx, fpx, err = filter_subnormal(x, fx, fpx, err)


    title = "{} Error for {} input {}".format(typ, approx_fname, input_typ)

    # Plot of function
    fig, ax1 = plt.subplots()

    # Plot of error
    ax2 = ax1.twinx()

    # Labels
    ax1.set_title(title)
    ax1.set_xlabel("Input")
    ax1.set_ylabel("Output")
    ax2.set_ylabel("Error")

    # Set y range for tan
    if fx[0] == "Tan" and (x[-1] - x[2]) > 3.14:
        ax1.set_ylim([-3.0, 3.0])

    # Zero error
    ax2.axhline(0, color="#FF00FF", linewidth=1)

    # 1/2 ULP from zero error
    if abs_err == False:
        ax2.axhline(1.1102230246251565e-16, color="#FF4500", linewidth=1)
        ax2.axhline(-1.1102230246251565e-16, color="#FF4500", linewidth=1)

    # Error
    ax2.scatter(x[1:], err[1:], s=1, color="red")

    # y=0
    if any(i<=0.0 for i in x[1:]) and any(i>=0.0 for i in x[1:]):
        ax1.axvline(0, color="black", linewidth=1)

    # x=0
    if any(i<=0.0 for i in fx[1:]) and any(i>=0.0 for i in fx[1:]):
        ax1.axhline(0, color="black", linewidth=1)

    # Approximation
    ax1.scatter(x[1:], fpx[1:], s=1, color="purple")

    # Oracle
    ax1.scatter(x[1:], fx[1:], s=0.5, color="blue")

    # Bigger image
    fig.set_size_inches(6.4*2, 4.8*2)

    fname = "{}.png".format(title.replace(" ", "_"))
    fname = path.join(in_dir, fname)
    print("  Saving: {}".format(fname))
    fig.savefig(fname)
    plt.close()

    abserr = [abs(e) for e in err[1:]]
    maxabserr = max(abserr)
    avgabserr = sum(abserr)/len(abserr)
    print("    Max absolute value of error: {}".format(maxabserr))
    print("    Avg absolute value of error: {}".format(avgabserr))


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
    fname = argv[1]

    in_dir = path.split(fname)[0]
    parts = fname.split("_")
    input_typ = parts[-1].split(".")[0]

    columns = read_dat(fname)

    print("Plotting: {} (~correct rounding for whole expression)".format(columns[1][0]), flush=True)
    plot_error(in_dir, input_typ, columns[0], columns[1], columns[1], columns[2], True)
    for i in range(4, len(columns), 3):
        print("Plotting: {}".format(columns[i][0]), flush=True)
        plot_error(in_dir, input_typ, columns[0], columns[1], columns[i], columns[i+1], True)
        #plot_error(in_dir, input_typ, columns[0], columns[1], columns[i], columns[i+2], False)



if __name__ == "__main__":
    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
