from time import perf_counter


class StageTimer:

    def __enter__(self):

        self.start = perf_counter()

        return self

    def __exit__(self, *args):

        self.end = perf_counter()

        self.elapsed = self.end - self.start