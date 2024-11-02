from abc import ABC, abstractmethod


class VisualElement(ABC):

    def __init__(self, element):
        self.element = element

    @abstractmethod
    def plot_element(self):
        raise

    @abstractmethod
    def plot_global_displacement(self, scale):
        raise NotImplementedError
