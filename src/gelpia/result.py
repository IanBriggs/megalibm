

from utils.logging import Logger
from utils.timing import Timer
from math import isinf
from multiprocessing import Process, Value

import gelpia
import gelpia_logging
import time


logger = Logger(level=Logger.HIGH, color=Logger.green)
timer = Timer()


class GelpiaInfError(Exception):
    def __init__(self, query):
        self.query = query


CACHE = dict()


class GelpiaResult():

    # Setup logging to avoid runtime error
    gelpia_logging.set_log_filename(None)

    # Silence gelpia
    gelpia_logging.set_log_level(-10)

    # Setup gelpia's env
    gelpia.setup_requirements(git_dir=gelpia.GIT_DIR)

    # Setup rust's env
    RUST_EXECUTABLE = gelpia.setup_rust_env(git_dir=gelpia.GIT_DIR,
                                            debug=False)

    # Tell gelpia how hard to try
    CONFIG = {
        "epsilons": (0.2, 0.2, 0.1),
        "timeout": 60,
        "grace": 0,
        "update": 0,
        "iters": 0,
        "seed": 42,
        "debug": False,
        "src_dir": gelpia.SRC_DIR,
        "executable": RUST_EXECUTABLE,
    }

    def __init__(self, query):
        self.query = query

        if self.query in CACHE:
            cached = CACHE[self.query]
            self.max_lower = cached.max_lower
            self.max_upper = cached.max_upper
            self.min_lower = cached.min_lower
            self.min_upper = cached.min_upper
            self.abs_max = cached.abs_max
            return

        timer.start()

        # Run and set results as member
        max_lower = Value("d", float("nan"))
        max_upper = Value("d", float("nan"))
        max_args = {"function": self.query,
                    "max_lower": max_lower,
                    "max_upper": max_upper}
        max_args.update(GelpiaResult.CONFIG)
        p = Process(target=gelpia.find_max, kwargs=max_args)

        p.start()

        self.min_lower, self.min_upper = gelpia.find_min(function=self.query,
                                                         **GelpiaResult.CONFIG)

        p.join()

        timer.stop()

        self.max_lower = max_lower.value
        self.max_upper = max_upper.value
        self.abs_max = max(self.max_upper, -self.min_lower)

        if isinf(self.abs_max):
            raise GelpiaInfError(self.query)

        CACHE[self.query] = self

