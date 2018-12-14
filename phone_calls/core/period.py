class Period:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_inside(self, start=None, end=None):
        return start <= self.start <= self.end <= end

    def is_moment_inside(self, moment):
        return self.start <= moment <= self.end

    def seconds_diff(self):
        return (self.end - self.start).total_seconds()
