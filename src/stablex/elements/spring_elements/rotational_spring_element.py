import numpy as np

from stablex import Node
from stablex.elements.spring_elements.spring_element import SpringElement
from stablex.degree_of_freedom import DegreeOfFreedom


class LinearRotationalSpringElement(SpringElement):
    """
    Represents a linear rotational spring element between two nodes.

    This class implements the behavior of a linear rotational spring,
    defining its stiffness characteristics and transformation for structural analysis.

    Parameters
    ----------
    start_node : Node
        The starting node of the spring element.
    end_node : Node
        The ending node of the spring element.
    rotational_stiffness : float
        The rotational stiffness of the spring element.

    Attributes
    ----------
    rotational_stiffness : float
        The rotational stiffness of the spring element.
    stiffness_matrix_dofs : list
        The degrees of freedom associated with the stiffness matrix of the element.
    """
    def __init__(self, start_node: Node, end_node: Node, rotational_stiffness):
        super().__init__(start_node, end_node)
        self._rotational_stiffness = rotational_stiffness

    def first_order_elastic_stiffness_matrix(self):
        """
        Computes the first-order elastic stiffness matrix for the spring element.

        Returns
        -------
        np.ndarray
            A 2x2 elastic stiffness matrix representing the rotational spring behavior.
        """
        k = self.rotational_stiffness
        return k * np.array([[1, -1],
                             [-1, 1]])

    def geometric_stiffness_matrix(self, end_forces: np.ndarray):
        """
        Computes the geometric stiffness matrix for the spring element.

        Currently returns a zero matrix, as the spring is assumed linear elastic.

        Parameters
        ----------
        end_forces : np.ndarray
            The forces at the ends of the spring element.

        Returns
        -------
        np.ndarray
            A 2x2 geometric stiffness matrix.
        """
        return np.array([[0, 0],
                         [0, 0]])

    def transformation_matrix(self):
        """
        Defines the transformation matrix for the spring element.

        Returns
        -------
        np.ndarray
            A 2x2 transformation matrix for the spring element.
        """
        return np.array([[1, 0],
                         [0, 1]])

    @property
    def rotational_stiffness(self):
        """
        Gets the rotational stiffness of the spring element.

        Returns
        -------
        float
            The rotational stiffness value.
        """
        return self._rotational_stiffness

    @rotational_stiffness.setter
    def rotational_stiffness(self, value):
        """
        Sets the rotational stiffness of the spring element.

        Parameters
        ----------
        value : float
            The new rotational stiffness value. Must be a positive number.

        Raises
        ------
        ValueError
            If the provided value is not positive.
        """
        if value <= 0:
            raise ValueError("Rotational stiffness must be a positive value.")
        self._rotational_stiffness = value

    @property
    def stiffness_matrix_dofs(self) -> list[DegreeOfFreedom]:
        """
        Gets the degrees of freedom associated with the stiffness matrix of the element.

        Returns
        -------
        list[DegreeOfFreedom]
            A list of degrees of freedom for the spring element.
        """
        return [self.start_node.rz_dof, self.end_node.rz_dof]
