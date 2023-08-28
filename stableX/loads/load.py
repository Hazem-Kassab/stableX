from abc import ABC, abstractmethod


class Load(ABC):

    def __init__(self, magnitude):
        self.magnitude = magnitude

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, value):
        self._magnitude = value


    