from abc import abstractmethod, ABC


class Section(ABC):
    """
        Abstract base class representing a structural section.

        This class defines the basic properties and methods that all specific
        section types must implement.

        Properties
        ----------
        area : float
            The cross-sectional area of the section (to be implemented in subclasses).
        inertia : float
            The moment of inertia of the section (to be implemented in subclasses).
        radius_of_gyration : float
            The radius of gyration, calculated as the square root of the ratio of the
            moment of inertia to the cross-sectional area.

        Notes
        -----
        The radius of gyration provides a measure of the distribution of cross-sectional
        area around the axis of bending.
        """
    @property
    @abstractmethod
    def area(self) -> float:
        """Gets the cross-sectional area of the section."""
        raise NotImplementedError

    @property
    @abstractmethod
    def inertia(self) -> float:
        """Gets the moment of inertia of the section."""
        raise NotImplementedError

    @property
    def radius_of_gyration(self) -> float:
        """Calculates the radius of gyration."""
        return (self.inertia / self.area) ** 0.5 if self.area != 0 else 0


class Rectangle(Section):
    """
        Represents a rectangular structural section.


        Attributes
        ----------
        width : float
            The width of the rectangle.
        height : float
            The height of the rectangle.

        Properties
        ----------
        area : float
            Calculates and returns the area of the rectangle.
        inertia : float
            Calculates and returns the moment of inertia of the rectangle  about its major centroidal axis.

        """
    def __init__(self, width: float, height: float):
        """
        Initializes a new rectangular section with the specified width and height.

        Parameters
        ----------
        width : float
            The width of the rectangle.
        height : float
            The height of the rectangle.
        """
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        """Calculates and returns the area of the rectangle."""
        return self.width * self.height

    @property
    def inertia(self) -> float:
        """Calculates and returns the moment of inertia of the rectangle about its centroidal axis."""
        return (self.width * self.height ** 3) / 12


class UserDefinedSection(Section):

    def __init__(self, area: float, inertia: float):
        """
         Initializes a new user-defined section with the specified area and inertia.

         Parameters
         ----------
         area : float
             The cross-sectional area of the section.
         inertia : float
             The moment of inertia of the section.
         """
        self._area = area
        self._inertia = inertia

    @property
    def inertia(self) -> float:
        """Gets the cross-sectional area of the section."""
        return self._inertia

    @inertia.setter
    def inertia(self, value: float):
        """Sets the cross-sectional area of the section."""
        self._inertia = value

    @property
    def area(self) -> float:
        """Gets the moment of inertia of the section."""
        return self._area

    @area.setter
    def area(self, value: float):
        """Sets the moment of inertia of the section."""
        self._area = value
