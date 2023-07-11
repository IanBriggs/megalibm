
import datetime
import os.path as path
import sys

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os
import argparse
import json

# Main result
libm_color = "#009900"
megalibm_colour = "sandybrown" #"#FC4C02" 
ruler_colour = "mediumblue" #"#0000FF"

def pareto_front_points(xs, ys):
    points = list(zip(xs, ys))
    points.sort(key=lambda p: p[0])

    if len(points) == 0:
        return [[],[]]
    pareto_points = [points[0]]
    for p in points:
        if p[1] > pareto_points[-1][1]:
            pareto_points.append(p)

    return [p[0] for p in pareto_points], [p[1] for p in pareto_points]


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


def plot_pareto_front(title, benchmark_data):
    out_name = "{}_pareto.png".format(title.replace(" ", "_"))
    print(f"Plotting: {out_name}")

    # Get names
    
    ruler_data = benchmark_data[0]
    megalibm_data = benchmark_data[1]
    

    if megalibm_data is not None:
        bench_name = megalibm_data["error"]["name"]
        libm_name = f"libm_{bench_name}"
        
        # Get baseline data
        libm_time = megalibm_data["timing"]["functions"][libm_name]["avg_time_per_sample"]
        libm_err = max(megalibm_data["error"]
                       ["functions"][libm_name]["rel_max_errors"])
    else:
        bench_name = ruler_data["error"]["name"]
        libm_name = f"libm_{bench_name}"
        
        # Get baseline data
        libm_time = ruler_data["timing"]["functions"][libm_name]["avg_time_per_sample"]
        libm_err = max(ruler_data["error"]
                       ["functions"][libm_name]["rel_max_errors"])
    

    
    # Get megalibm baseline data
    if megalibm_data is not None:
        megalibm_names = [k for k in megalibm_data["timing"]["functions"]
                 if k != libm_name]
        
        megalibm_times = [megalibm_data["timing"]["functions"][name]["avg_time_per_sample"]
                     for name in megalibm_names]
        megalibm_errs = [max(megalibm_data["error"]["functions"][name]["rel_max_errors"])
                    for name in megalibm_names]
    else:
        megalibm_times = []
        megalibm_errs = []

    # Get ruler data
    if ruler_data is not None:
        ruler_names = [k for k in ruler_data["timing"]["functions"]
                 if k != libm_name]
        
        ruler_times = [ruler_data["timing"]["functions"][name]["avg_time_per_sample"]
                     for name in ruler_names]
        ruler_errs = [max(ruler_data["error"]["functions"][name]["rel_max_errors"])
                    for name in ruler_names]
    else:
        ruler_times = []
        ruler_errs = []


    # Normalize so libm = [1,1]
    ruler_speedup_s = list([libm_time / t for t in ruler_times])
    ruler_errup_s = list([e / libm_err for e in ruler_errs])
    megalibm_speedup_s = list([libm_time / t for t in megalibm_times])
    megalibm_errup_s = list([e / libm_err for e in megalibm_errs])
    libm_time = 1.0
    libm_err = 1.0


    # Determine pareto points
    ruler_pareto_xs, ruler_pareto_ys = pareto_front_points(
        ruler_errup_s, ruler_speedup_s)
    megalibm_pareto_xs, megalibm_pareto_ys = pareto_front_points(
        megalibm_errup_s, megalibm_speedup_s)

    # Make the stepped line points
    ruler_pareto_step_xs = double_list(ruler_pareto_xs)
    ruler_pareto_step_xs = ruler_pareto_step_xs[1:]
    ruler_pareto_step_ys = double_list(ruler_pareto_ys)
    ruler_pareto_step_ys = ruler_pareto_step_ys[:-1]
    
    # ruler_pareto_step_xs = ruler_pareto_xs
    # ruler_pareto_step_ys = ruler_pareto_ys
    
    megalibm_pareto_step_xs = double_list(megalibm_pareto_xs)
    # megalibm_pareto_step_xs = megalibm_pareto_xs
    megalibm_pareto_step_xs = megalibm_pareto_step_xs[1:]
    megalibm_pareto_step_ys = double_list(megalibm_pareto_ys)
    # megalibm_pareto_step_ys = megalibm_pareto_ys
    megalibm_pareto_step_ys = megalibm_pareto_step_ys[:-1]

    # Plot
    fig = plt.figure()
    ax1 = fig.add_subplot()

    # Data
    libm = ax1.scatter([libm_err], [libm_time], color=libm_color)
    megalibm = ax1.scatter(megalibm_errup_s, megalibm_speedup_s, color=megalibm_colour, marker="D")
    ax1.plot(megalibm_pareto_step_xs, megalibm_pareto_step_ys, color=megalibm_colour, lw=1.3)
    # ax1.plot(megalibm_pareto_step_xs, megalibm_pareto_step_ys, color=megalibm_colour)

    ruler = ax1.scatter(ruler_errup_s, ruler_speedup_s, color=ruler_colour, marker="*")
    ax1.plot(ruler_pareto_step_xs, ruler_pareto_step_ys, color=ruler_colour, lw=0.7)
    # ax1.plot(ruler_pareto_step_xs, ruler_pareto_step_ys, '-', color=ruler_colour)

    
    # Scale
    ax1.set_xscale('log')
    ax1.invert_xaxis()

    # Labels
    stripped_title = title[0:title.index("domain ") + len("domain ")]
    detailed_title = stripped_title + domain_name(benchmark_data[0])
    ax1.set_title(detailed_title)
    ax1.set_xlabel("Maximum Relative Error")
    ax1.set_ylabel("Speedup vs libm")

    # legend
    ax1.legend([libm, megalibm, ruler], ['Libm', 'Megalibm', 'Renumo'])


    # Set ratio and size
    scale = 0.7
    fig.set_size_inches(6.4 * scale, 4 * scale)
    # fig.set_size_inches(6.4 * scale, 4.8 * scale)
    fig.tight_layout()

    # Save and close
    plt.savefig("results/plots/" + out_name, dpi=100)
    plt.close()

    return out_name


def read_data_local(ruler, megalibm):

    result = [None, None]
    for mode, dirname in enumerate([ruler, megalibm]):
        print("Reading from directory: {}", dirname)
        benchmark_data = dict()
        for i in range(4):
            benchmark_data[i] = dict()
    
            # For the two measurement types
            for type in ["error", "timing"]:
            
                # Read the file
                
                fname = f"{dirname}{type}_data_{i}.json"
                print("  {}", fname)

                try: 
                    with open(fname, 'r') as f:

                        page = f.read()
                        one_run = json.loads(page)
                        # print(one_run)
                        # with open(f"oopsla23/{mode}/{fname.split('/')[-2] + '/' + fname.split('/')[-1]}", "w") as f:
                        #    f.write(json.dumps(one_run))

                        benchmark_data[i][type] = one_run
                        # print(f"I made it with {dirname} and {i}, {type}")

                        # Since json doesn't like nan, we encode nan as a string
                        # print("this is one run")
                        # print(one_run)
                        if type == "error":
                            for fname in one_run["functions"]:
                                for dname in one_run["functions"][fname]:
                                    data = one_run["functions"][fname][dname]
                                    data = [float(item) for item in data]
                                    one_run["functions"][fname][dname] = data
                except FileNotFoundError:
                    print(f"{fname} does not exist!")
    
        # Light data validation
        # print(benchmark_data)
        # print(i)
        # print(result)
        if "error" in benchmark_data[0]:
            name = benchmark_data[0]["error"]["name"]
            print(name)
            body = benchmark_data[0]["error"]["body"]
            for domain, data in benchmark_data.items():
                for type, data in data.items():
                    assert name == data["name"], "Wrong name!"
                    assert body == data["body"], "Wrong body!"
            # print(benchmark_data[0].keys())
            result[mode] = benchmark_data
            # print(result[mode][0].keys())

    # print("will ret")
    # print(result[0][0].keys())

    return (result[0], result[1])



def make_main_part(benchmark_name, pareto_images):
    name = benchmark_name
    pareto_0 = pareto_images[benchmark_name][0]
    pareto_1 = pareto_images[benchmark_name][1]
    pareto_2 = pareto_images[benchmark_name][2]
    pareto_3 = pareto_images[benchmark_name][3]
    return f"""
    <div class="rounded-box result-box">
        <div class="result-quad">
            <div class="row">
                <div class="plot">
                    <img class="plot-image" src="plots/{pareto_0}">
                </div>
                <div class="plot">
                    <img class="plot-image" src="plots/{pareto_1}">
                </div>
            </div>
            <div class="row">
                <div class="plot">
                    <img class="plot-image" src="plots/{pareto_2}">
                </div>
                <div class="plot">
                    <img class="plot-image" src="plots/{pareto_3}">
                </div>
            </div>
        </div>
    </div>
    """.rstrip()


def make_main_page(benchmark_names, pareto_images ):
    today = datetime.date.today()
    y = today.year
    m = today.month
    d = today.day

    parts = []

    for bench_name in benchmark_names:
        parts.append(make_main_part(bench_name, pareto_images))

    parts.append("""
    </body>
    </html>
    """.replace("\n    ", "\n").strip())

    
    parts.append("""<style>
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
    </style>
    """.replace("\n    ", "\n").strip())

    text = "\n".join(parts)

    return text


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument("-d", "--directory",
                        type=str,
                        help="Load results from given directory.")
    # parser.add_argument("dirname",
    #                     help="Directory with the generated functions and data")
    args = parser.parse_args(argv[1:])

    # Logger.set_log_level(Logger.str_to_level(args.verbosity))

    # if args.log_file is not None:
    #     Logger.set_log_filename(args.log_file)

    # logger.dlog("Settings:")
    # logger.dlog("    dirname: {}", args.dirname)
    # logger.dlog("  verbosity: {}", args.verbosity)
    # logger.dlog("   log-file: {}", args.log_file)
    # return None

    return args

def main(argv):
    # data location should be latest run... e.g. http://nightly.cs.washington.edu/reports/megalibm/1679665857/generated/core_function_asin/error_data_1.json
    args = parse_arguments(argv)
    
    # 1679665857

    base_ruler = args.directory
    
    # need to have an option to run fresh 
    # base_ruler = "oopsla23/tool/"
    base_megalibm = "oopsla23/megalibm/"

    benchmark_names = list()
    benchmarks_datas = dict()
    pareto_images = dict()
    value_images = dict()

    ext = '/'

    def listFD(base, ext=''):
        # page = requests.get(base).text
        # print(page)
        # soup = BeautifulSoup(page, 'html.parser')
        # return [node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
        return os.listdir(base)

    list_ruler = listFD(base_ruler, ext)
    list_megalibm = listFD(base_megalibm, ext)

    benchmarks = list(set([f"{x}/" for x in list_ruler + list_megalibm]))
    print(benchmarks)

    # # Look through directory contents
    for name in sorted(benchmarks):
        if ".." in name:
            continue
        # os.chdir(base)

        # Skip non-directories
        # if not path.isdir(name):
        #     print("Skipping: {}", name)
        #     continue

        # Read data for the benchmark

        # try to get both, if it fails, then oh well
        print(name)
        ruler = base_ruler + name
        megalibm = base_megalibm + name
        ruler_benchmark_data, megalibm_benchmark_data = read_data_local(ruler, megalibm)

        only_name = name.split("/")[-2]
        print(name.split("/"))
        # Setup collections
        benchmark_names.append(name)
        pareto_images[name] = dict()
        value_images[name] = dict()

        # os.chdir(name)

        # Plot images
        # print(ruler_benchmark_data)
        # print(megalibm_benchmark_data)
        if megalibm_benchmark_data is None:
            data = ruler_benchmark_data.keys()
            print("clear")
            print(ruler_benchmark_data[0].keys())
            result = lambda x: (ruler_benchmark_data[x], None)
        elif ruler_benchmark_data is None:
            data = megalibm_benchmark_data.keys()
            result = lambda x: (None, megalibm_benchmark_data[x])
        elif ruler_benchmark_data is not None and megalibm_benchmark_data is not None: 
            data = (ruler_benchmark_data.keys() | megalibm_benchmark_data.keys())
            result = lambda x: (ruler_benchmark_data[x], megalibm_benchmark_data[x])

        # print(data)
        for key in data: #TODO not sure if this was entirely right as it was iterating over idx, items = .items() previously
            try:
                image_name  = plot_pareto_front(
                    f"{only_name} domain {key}", result(key))
            except ZeroDivisionError:
                image_name = "does_not_exist"
            pareto_images[name][key] = image_name
            

    # Make webpages
    html = make_main_page(benchmark_names, pareto_images)
    print("Writing pareto.html")
    with open("results/pareto.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    return_code = 0
    try:
        return_code = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(return_code)