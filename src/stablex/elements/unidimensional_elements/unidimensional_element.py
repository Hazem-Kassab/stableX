from abc import ABC, abstractmethod
from stablex.elements.element import Element
from stablex.node import Node
from stablex.section import Section
from stablex.degree_of_freedom import DegreeOfFreedom


class UniDimensionalElement(Element, ABC):
    """
    Abstract base class for a unidimensional finite element, representing elements with two
    nodes and a defined cross-sectional area. Inherits from `Element`.

    Attributes
    ----------
    start_node : Node
        The starting node of the element.
    end_node : Node
        The ending node of the element.
    section : Section
        The section object containing the cross-sectional properties of the element.
    geometric_nonlinearity : bool
        Whether geometric nonlinearity is included in the element.
    elasticity_modulus : float
        The modulus of elasticity for the element material.
    length : float
        The length of the element calculated based on the coordinates of the start and end nodes.

    Methods
    -------
    transformation_matrix()
        Abstract method to define the transformation matrix for the element.
    shape_function(x)
        Abstract method to compute the shape function at a given local coordinate x.
    b_matrix(x)
        Abstract method to compute the strain-displacement matrix at local coordinate x.
    get_x_from_normal_coord(xi)
        Abstract method to calculate the physical x-coordinate from a given normalized coordinate.
    normal_b_matrix(xi)
        Abstract method to compute the strain-displacement matrix for a normalized coordinate.
    stiffness_matrix_dofs() -> list
        Abstract method to define degrees of freedom for the element's stiffness matrix.
    get_local_displacement(x)
        Calculates the local displacement at a given x-coordinate based on the shape function.

    Notes
    -----
    This class requires implementation of several abstract methods to define behavior specific
    to unidimensional elements.

    """

    def __init__(self, start_node: Node, end_node: Node, section: Section, include_geom_nonlinearity=False, elasticity_modulus=200000):
        """
        Initializes a UniDimensionalElement instance.

        Parameters
        ----------
        start_node : Node
            The starting node of the element.
        end_node : Node
            The ending node of the element.
        section : Section
            The cross-sectional area and properties of the element.
        include_geom_nonlinearity : bool, optional
            Indicates whether geometric nonlinearity should be considered (default is False).
        elasticity_modulus : float, optional
            Elasticity modulus of the element material, in consistent units (default is 200,000).
        """

        super().__init__(start_node, end_node, include_geom_nonlinearity)
        self._start_node = start_node
        self._end_node = end_node
        self._section = section
        self.elasticity_modulus = elasticity_modulus

    @property
    def length(self) -> float:
        """
        float: The length of the element, computed based on the Euclidean distance between
        the start and end nodes.
        """
        return ((self.end_node.x - self.start_node.x) ** 2 +
                (self.end_node.y - self.start_node.y) ** 2) ** 0.5

    @property
    def section(self) -> Section:
        """Section: The cross-sectional properties of the element."""
        return self._section

    @section.setter
    def section(self, value: Section):
        """Sets a new section for the element."""
        self._section = value

    @abstractmethod
    def transformation_matrix(self):
        """Abstract method for defining the transformation matrix of the element."""
        raise NotImplementedError

    @abstractmethod
    def shape_function(self, x):
        """
        Abstract method to calculate the shape function at a given local coordinate.

        Parameters
        ----------
        x : float
            The local coordinate at which to compute the shape function value.
        """
        raise NotImplementedError

    @abstractmethod
    def b_matrix(self, x):
        """
        Abstract method to compute the strain-displacement matrix at a given local coordinate.

        Parameters
        ----------
        x : float
            The local coordinate at which to compute the strain-displacement matrix.
        """
        raise NotImplementedError

    @abstractmethod
    def get_x_from_normal_coord(self, xi):
        """
        Abstract method to calculate the physical x-coordinate from a given normalized coordinate.

        Parameters
        ----------
        xi : float
            The normalized coordinate for which to compute the physical x-coordinate.
        """
        raise NotImplementedError

    @abstractmethod
    def normal_b_matrix(self, xi):
        """
        Abstract method to compute the strain-displacement matrix for a normalized coordinate.

        Parameters
        ----------
        xi : float
            The normalized coordinate for which to compute the strain-displacement matrix.
        """
        raise NotImplementedError

    @abstractmethod
    def stiffness_matrix_dofs(self) -> list[DegreeOfFreedom]:
        """Defines the degrees of freedom for the element's stiffness matrix."""
        pass

    def get_local_displacement(self, x):
        """Defines the degrees of freedom for the element's stiffness matrix."""
        return self.shape_function(x).dot(self.local_end_displacements())
