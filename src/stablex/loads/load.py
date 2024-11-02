from abc import ABC, abstractmethod


class Load(ABC):
    """
    Abstract base class for representing loads in the structural analysis model.

    .. note::
        This class is not yet used in this release but is planned for future development
        to represent various types of loads applied to elements or nodes.

    Parameters
    ----------
    magnitude : float
        The magnitude of the load applied to an element or node.

    Attributes
    ----------
    magnitude : float
        Represents the magnitude of the load. Can be set to update the load's value.
    """
    def __init__(self, magnitude):
        self.magnitude = magnitude

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, value):
        self._magnitude = value

