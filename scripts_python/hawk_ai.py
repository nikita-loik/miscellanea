import numpy as np

class RunningMetrics():
    def __init__(self):
        self._x = 0
        self._count = 0
        self._mean = 0
        self._deviation_from_the_mean = 0
        self._std = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    def update(self):
        self._count += 1

        self._deviation_from_the_mean = self._x - self._mean

        new_mean = self._mean + (self._deviation_from_the_mean) / self._count
        new_std = self._std + (self._deviation_from_the_mean) * (self._x - new_mean)

        self._mean = new_mean
        self._std = new_std

    @property
    def mean(self):
        return self._mean

    @property
    def deviation_from_the_mean(self):
        return self._deviation_from_the_mean

    @property
    def std(self):
        if self._count == 1:
            return 0
        return np.sqrt(self._std / (self._count - 1))