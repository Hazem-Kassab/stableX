from abc import abstractmethod, ABC

import numpy as np

from src.stablex import Node


class Element(ABC):
    """
    Abstract base class representing a finite element in structural analysis.

    Parameters
    ----------
    start_node : Node
        The starting node of the element.
    end_node : Node
        The ending node of the element.
    include_geom_nonlinearity : bool, optional
        Indicates whether geometric nonlinearity should be considered (default is False).

    Attributes
    ----------
    start_node : Node
        The starting node of the element, modifiable after initialization.
    end_node : Node
        The ending node of the element, modifiable after initialization.
    geometric_nonlinearity : bool
        Whether geometric nonlinearity is included in the element.
    id : int
        Unique identifier for the element instance, auto-incremented.
    stiffness_matrix : np.ndarray
        The stiffness matrix for the element.

    Properties
    ----------
    nodes : set of Node
        Returns a set containing the start and end nodes of the element.
    stiffness_matrix_dofs : list
        List of degrees of freedom for the stiffness matrix, must be implemented by subclasses.

    Methods
    -------
    first_order_elastic_stiffness_matrix()
        Abstract method to compute the first-order elastic stiffness matrix.
    geometric_stiffness_matrix(end_forces: np.ndarray)
        Abstract method to compute the geometric stiffness matrix based on end forces.
    b_matrix(*args)
        Placeholder method for computing the strain-displacement matrix, if applicable.
    transformation_matrix()
        Abstract method to obtain the transformation matrix for the element.
    global_stiffness_matrix() -> np.ndarray
        Computes the global stiffness matrix for the element.
    global_end_displacements() -> np.ndarray
        Returns the global end displacements based on degree of freedom displacements.
    local_end_displacements() -> np.ndarray
        Computes the local end displacements using the transformation matrix.
    local_end_forces() -> np.ndarray
        Calculates the local end forces based on the stiffness matrix and displacements.
    global_end_forces() -> np.ndarray
        Computes the global end forces by transforming the local forces.

    Notes
    -----
    This class serves as a base class for specific element types and requires the implementation
    of several abstract methods and properties to define the stiffness and transformation matrices.
    """
    id_counter = 1

    def __init__(self, start_node: Node, end_node: Node, include_geom_nonlinearity=False):
        """
        Initializes an Element instance with specified start and end nodes.

        Parameters
        ----------
        start_node : Node
            The starting node of the element.
        end_node : Node
            The ending node of the element.
        include_geom_nonlinearity : bool, optional
            Indicates whether geometric nonlinearity should be considered (default is False).

        Notes
        -----
        This class serves as a base class for specific element types and requires the implementation
        of several abstract methods and properties to define the stiffness and transformation matrices.

        The id attribute is auto-incremented with each new instance created.
        """
        self._start_node = start_node
        self._end_node = end_node
        self.geometric_nonlinearity = include_geom_nonlinearity
        self.id = Element.id_counter
        self._stiffness_matrix = np.zeros((len(self.stiffness_matrix_dofs), len(self.stiffness_matrix_dofs)))
        Element.id_counter += 1

    @property
    def nodes(self):
        """Returns a set containing the start and end nodes of the element."""
        return {self.start_node, self.end_node}

    @property
    @abstractmethod
    def stiffness_matrix_dofs(self) -> list:
        """List of degrees of freedom for the stiffness matrix, implemented by subclasses."""
        raise NotImplementedError

    @property
    def start_node(self) -> Node:
        """Node: The starting node of the element, defining one end of the element's length."""
        return self._start_node

    @start_node.setter
    def start_node(self, value: Node):
        """Sets the starting node of the element."""
        self._start_node = value

    @property
    def end_node(self) -> Node:
        """Node: The ending node of the element, defining the other end of the element's length."""
        return self._end_node

    @end_node.setter
    def end_node(self, value: Node):
        """Sets the ending node of the element."""
        self._end_node = value

    @abstractmethod
    def first_order_elastic_stiffness_matrix(self):
        """Computes the first-order elastic stiffness matrix."""
        raise NotImplementedError

    @abstractmethod
    def geometric_stiffness_matrix(self, end_forces: np.ndarray):
        """Computes the geometric stiffness matrix based on end forces."""
        raise NotImplementedError

    @property
    def stiffness_matrix(self):
        """
        np.ndarray: The combined stiffness matrix of the element, representing the sum of the
        elastic and geometric stiffness matrices.
        """
        return self._stiffness_matrix

    @stiffness_matrix.setter
    def stiffness_matrix(self, value: np.ndarray):
        self._stiffness_matrix = value

    def b_matrix(self, *args):
        """Placeholder method for computing the strain-displacement matrix, if applicable."""
        raise NotImplementedError

    @abstractmethod
    def transformation_matrix(self):
        """Obtains the transformation matrix for the element."""
        raise NotImplementedError

    def global_stiffness_matrix(self):
        """Computes the global stiffness matrix for the element."""
        return self.transformation_matrix().T.dot(self.stiffness_matrix).dot(self.transformation_matrix())

    def global_end_displacements(self):
        """Returns the global end displacements based on degree of freedom displacements."""
        return np.array([dof.displacement for dof in self.stiffness_matrix_dofs])

    def local_end_displacements(self):
        """Computes the local end displacements using the transformation matrix."""
        return self.transformation_matrix().dot(self.global_end_displacements())

    def local_end_forces(self):
        """Calculates the local end forces based on the stiffness matrix and displacements."""
        return self.stiffness_matrix.dot(self.local_end_displacements())

    def global_end_forces(self):
        """Computes the global end forces by transforming the local forces."""
        return self.transformation_matrix().T.dot(self.local_end_forces())

