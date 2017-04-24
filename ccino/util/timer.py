import sys


PYTHON_3_3 = sys.version_info[0] == 3 and sys.version_info[1] >= 3


if PYTHON_3_3:
    from time import perf_counter
else:
    from time import clock


class Timer(object):
    def start(self):
        if PYTHON_3_3:
            self._start = perf_counter()
        else:
            self._start = clock()

    def stop(self):
        if PYTHON_3_3:
            self._time = perf_counter() - self._start
        else:
            self._time = clock() - self._start

    def get_time(self):
        return self._time
