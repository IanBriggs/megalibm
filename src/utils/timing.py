

import math
import time


class Timer():
    __slots__ = ["_times", "_start"]

    def __init__(self):
        self.reset()

    def __len__(self):
        return len(self._times)

    def reset(self):
        self._times = list()
        self._start = None

    def start(self):
        assert (self._start is None)
        self._start = time.perf_counter()

    def stop(self):
        assert (self._start is not None)
        self._times.append(time.perf_counter() - self._start)
        self._start = None
        return self._times[-1]

    def elapsed(self):
        assert (self._start is None)
        elapsed = sum(self._times)
        return elapsed

    def average(self):
        assert (self._start is None)
        assert (len(self._times) >= 1)
        mean = self.elapsed() / len(self._times)
        return mean

    def stddev(self):
        assert (self._start is None)
        assert (len(self._times) >= 2)
        mean = self.average()
        diffs = [t-mean for t in self._times]
        squares = [d**2 for d in diffs]
        sum_of_squares = sum(squares)
        mean_of_squares = sum_of_squares / len(squares)
        sq_root = math.sqrt(mean_of_squares)
        return sq_root

    def minimum(self):
        assert (self._start is None)
        assert (len(self._times) >= 1)
        minimum = min(self._times)
        return minimum

    def maximum(self):
        assert (self._start is None)
        assert (len(self._times) >= 1)
        maximum = max(self._times)
        return maximum

    def median(self):
        assert (self._start is None)
        assert (len(self._times) >= 1)
        ordered = sorted(self._times)
        if len(ordered) % 2 == 1:
            middle = len(ordered)/2
            median = ordered[middle]
            return median
        middle_left = math.floor(len(ordered)/2)
        middle_right = middle_left + 1
        median_left = ordered[middle_left]
        median_right = ordered[middle_right]
        median = (median_left + median_right) / 2
        return median

    def times(self):
        assert (self._start is None)
        return self._times.copy()


def main(argv):
    iters = 10000000
    try:
        iters = int(argv[1])
    except IndexError:
        pass
    except ValueError:
        print(f"Ignoring non integer argument: '{argv[1]}'")

    total_start = time.perf_counter()

    my_timer = Timer()
    for _ in range(iters):
        my_timer.start()
        pass
        my_timer.stop()

    total_stop = time.perf_counter()

    loop_start = time.perf_counter()

    for _ in range(iters):
        pass

    loop_stop = time.perf_counter()

    iterations = len(my_timer)
    assert (iters == iterations)
    minimum = my_timer.minimum() * 1e9
    average = my_timer.average() * 1e9
    median = my_timer.median() * 1e9
    maximum = my_timer.maximum() * 1e9
    stddev = my_timer.stddev() * 1e9

    total_time = total_stop - total_start
    loop_overhead = loop_stop - loop_start
    timer_overhead = total_time - loop_overhead
    per_start_stop = timer_overhead / iters
    ns_per_start_stop = per_start_stop * 1e9

    print("Stats:")
    print(f" iterations: {iterations}")
    print(f"    minimum: {minimum:.6f} nsec")
    print(f"    average: {average:.6f} nsec")
    print(f"     median: {median:.6f} nsec")
    print(f"    maximum: {maximum:.6f} nsec")
    print(f"     stddev: {stddev:.6f} nsec")
    print()
    print("Overhead:")
    print(f"        total time: {total_time:.4f} sec")
    print(f"     loop overhead: {loop_overhead:.4f} sec")
    print(f"    timer overhead: {timer_overhead:.4f} sec")
    print(f" per pair overhead: {ns_per_start_stop:.4f} nsec")


if __name__ == "__main__":
    import sys

    return_code = 130  # meaning "Script terminated by Control-C"

    try:
        return_code = main(sys.argv)
    except KeyboardInterrupt:
        print("")
        print("Goodbye")

    sys.exit(return_code)
