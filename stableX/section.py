from abc import abstractmethod, ABC


class Section(ABC):

    @abstractmethod
    @property
    def area(self):
        raise NotImplementedError

    @abstractmethod
    @property
    def inertia(self):
        raise NotImplementedError

    @property
    def radius_of_gyration(self):
        return (self.inertia/self.area)*0.5


class Rectangle(Section):

    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def inertia(self):
        return self.width * self.height**3 / 12
