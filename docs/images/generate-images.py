#!/usr/bin/env python3

from math import pi, sin, cos, floor, log, exp
import matplotlib.pyplot as plt


lows = [pi/16 * i for i in range(8)]
highs = [pi/16 * i for i in range(1, 9)]
mids = [(l+h)/2 for l, h in zip(lows, highs)]
sin_table = [sin(m) for m in mids]
cos_table = [cos(m) for m in mids]


def table_sin(x):
    if 0 <= x < pi/2:
        idx = floor(x / (pi/16))
        return sin_table[idx]


def table_cos(x):
    if 0 <= x < pi/2:
        idx = floor(x / (pi/16))
        return cos_table[idx]

exp_lows = [log(2)/8 * i for i in range(8)]
exp_highs = [log(2)/8 * i for i in range(1, 9)]
exp_mids = [(l+h)/2 for l, h in zip(exp_lows, exp_highs)]
exp_table = [exp(m) for m in exp_mids]

def table_exp(x):
    if 0 <= x < log(2):
        idx = floor(x / (log(2)/8))
        return exp_table[idx]


def print_table():
    print(" low    | high   | sin((high+low)/2)")
    print("--------|--------|-------------------")
    for l, h, t in zip(lows, highs, sin_table):
        print(f" {str(l): <6.6} | {str(h): <6.6} | {str(t): <6.6}")


def plot_func(filename, x_min, x_max, y_min, y_max, func, approxs):
    samples = 25600
    x_width = x_max - x_min
    x_step = x_width / samples
    xs = [x_min + x_step*i for i in range(samples)]

    approx_ys = [[approx(x) for x in xs]
                 for approx in approxs]
    math_ys = [func(x) for x in xs]

    fig, ax = plt.subplots()

    plt.axhline(0, color="black")
    plt.axvline(0, color="black")

    ax.plot(xs, math_ys, alpha=0.4, linewidth=1.5)
    for ys in approx_ys:
        ax.plot(xs, ys, linewidth=0, marker=".", markersize=1.5)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    ax.plot()

    plt.savefig(filename, bbox_inches="tight")

    plt.close()


def poly_sin(x):
    return x - x*x*x/6


def mr_table_sin(x):
    new_x = x if (x < pi/2) else pi - x
    return table_sin(new_x)


def ml_table_cos(x):
    new_x = 0.0 - x if (x < 0.0) else x
    return table_cos(new_x)


def mr_mr_table_sin(x):
    new_x = x if (x < pi) else 2*pi - x
    return mr_table_sin(new_x)


def cmnr_mr_table_sin(x):
    new_x = x if (x < pi) else 2*pi - x
    y = mr_table_sin(new_x)
    new_y = y if (y is None or x < pi) else -y
    return new_y

def ar_cmnr_mr_table_sin(x):
    k = floor(x/(2*pi))
    new_x = x - k*2*pi
    return cmnr_mr_table_sin(new_x)

def exp_reduce_table_exp(x):
    k = floor(x / log(2))
    new_x = x - k*log(2)
    y = table_exp(new_x)
    new_y = y * 2.0**k
    return new_y


print_table()

plot_func("table_sin.png",
          -0.25*pi, 1.25*pi,
          -1.0625, 1.0625,
          sin, [table_sin])

plot_func("poly_sin.png",
          -0.25*pi, 1.25*pi,
                    -1.0625, 1.0625,
          sin, [poly_sin])

plot_func("mr_table_sin.png",
          -0.25*pi, 2.25*pi,
                    -1.0625, 1.0625,
          sin, [mr_table_sin,
                table_sin])

plot_func("ml_table_cos.png",
          -0.75*pi, 0.75*pi,
                    -1.0625, 1.0625,
          cos, [ml_table_cos,
                table_cos])

plot_func("mr_mr_table_sin.png",
          -0.25*pi, 2.25*pi,
                    -1.0625, 1.0625,
          sin, [mr_mr_table_sin,
                mr_table_sin])

plot_func("cmnr_mr_table_sin.png",
          -0.25*pi, 2.25*pi,
                    -1.0625, 1.0625,
          sin, [cmnr_mr_table_sin,
                mr_table_sin])

plot_func("ar_cmnr_mr_table_sin.png",
          -1.25*pi, 6.25*pi,
                    -1.0625, 1.0625,
          sin, [ar_cmnr_mr_table_sin,
                cmnr_mr_table_sin])


plot_func("exp_reduce_table_exp.png",
          -1.0, 2.0,
          0.0, 7.5,
          exp, [exp_reduce_table_exp,
                table_exp])