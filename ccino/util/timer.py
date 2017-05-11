import sys


PYTHON_3_3 = sys.version_info[0] == 3 and sys.version_info[1] >= 3


if PYTHON_3_3:
    from time import perf_counter
else:
    from time import clock


class Timer(object):
    """Simple timer that can be started and stopped."""

    def start(self):
        """Start the timer and wait for it to be stopped.

        Note:
            If the timer is started twice it will use the more recent
            time.
        """

        if PYTHON_3_3:
            self._start = perf_counter()
        else:
            self._start = clock()

    def stop(self):
        """Stop the timer.

        Note:
            If the timer is stopped twice it will use the more recent
            time.
        """

        if PYTHON_3_3:
            self._time = perf_counter() - self._start
        else:
            self._time = clock() - self._start

    def get_time(self):
        """Get the amount of time passed by the timer.

        Returns:
            float: The time elapsed.
        """

        return self._time
