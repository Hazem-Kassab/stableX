import numpy as np

from stablex.elements.unidimensional_elements.unidimensional_element import UniDimensionalElement
from stablex.degree_of_freedom import DegreeOfFreedom


class TrussElement(UniDimensionalElement):
    """
        Represents a truss element in a structural analysis model, inheriting from `UniDimensionalElement`.
        This element is characterized by two nodes and transmits only axial forces.

        Attributes
        ----------
        start_node : Node
            The starting node of the truss element.
        end_node : Node
            The ending node of the truss element.
        section : Section
            The cross-sectional properties of the element.
        geometric_nonlinearity : bool
            Whether geometric nonlinearity is included in the element.
        elasticity_modulus : float
            The modulus of elasticity for the truss element material.

        Methods
        -------
        stiffness_matrix_dofs() -> list[DegreeOfFreedom]
            Lists the degrees of freedom relevant to the truss element's stiffness matrix.
        transformation_matrix() -> np.ndarray
            Computes the transformation matrix for the element, based on its orientation.
        shape_function(x) -> np.ndarray
            Calculates the shape function at a specified local coordinate.
        first_order_elastic_stiffness_matrix() -> np.ndarray
            Computes the first-order elastic stiffness matrix for the truss element.
        geometric_stiffness_matrix(end_forces: np.ndarray) -> np.ndarray
            Calculates the geometric stiffness matrix for the element, based on axial forces.
        """

    @property
    def stiffness_matrix_dofs(self) -> list[DegreeOfFreedom]:
        """
        Returns the degrees of freedom for the truss element's stiffness matrix.

        Returns
        -------
        list[DegreeOfFreedom]
            A list of degrees of freedom objects, ordered as [start_node.x_dof, start_node.y_dof,
            end_node.x_dof, end_node.y_dof].
        """
        return [self.start_node.x_dof, self.start_node.y_dof,
                self.end_node.x_dof, self.end_node.y_dof]

    def transformation_matrix(self):
        """
        Computes the transformation matrix based on the element's orientation.

        Returns
        -------
        np.ndarray
            A 4x4 transformation matrix that aligns the element's local and global coordinates.
        """
        s = (self.end_node.y - self.start_node.y) / self.length
        c = (self.end_node.x - self.start_node.x) / self.length
        t = np.array([[c, s, 0, 0],
                      [-s, c, 0, 0],
                      [0, 0, c, s],
                      [0, 0, -s, c]])
        return t

    def shape_function(self, x):
        """
        Calculates the shape function at a specified local coordinate.

        Parameters
        ----------
        x : float
            The local coordinate along the element's length.

        Returns
        -------
        np.ndarray
            A 2x4 array representing the shape functions at the given local coordinate.
        """
        l = self.length
        return np.array([[1-x/l, 0, x/l, 0],
                         [0, 1-x/l, 0, x/l]])

    def b_matrix(self, x):
        """
        Abstract method placeholder to compute the strain-displacement matrix at a given local coordinate.

        Parameters
        ----------
        x : float
            The local coordinate along the element.
        """
        pass

    def get_x_from_normal_coord(self, xi):
        """
        Abstract method placeholder to calculate the physical x-coordinate from a normalized coordinate.

        Parameters
        ----------
        xi : float
            Normalized coordinate.
        """
        pass

    def normal_b_matrix(self, xi):
        """
        Abstract method placeholder to compute the strain-displacement matrix for a normalized coordinate.

        Parameters
        ----------
        xi : float
            Normalized coordinate.
        """
        pass

    def first_order_elastic_stiffness_matrix(self):
        """
        Computes the first-order elastic stiffness matrix for the truss element, based on elasticity
        modulus and cross-sectional area.

        Returns
        -------
        np.ndarray
            A 4x4 stiffness matrix for the truss element in its local coordinate system.
        """
        e = self.elasticity_modulus
        a = self.section.area
        l = self.length
        return e*a/l*np.array([[1, 0, -1, 0],
                               [0, 0, 0, 0],
                               [-1, 0, 1, 0],
                               [0, 0, 0, 0]])

    def geometric_stiffness_matrix(self, end_forces: np.ndarray):
        """
        Calculates the geometric stiffness matrix based on the axial forces in the element.

        Parameters
        ----------
        end_forces : np.ndarray
            A vector of end forces in the element, where end_forces[2] is the axial force.

        Returns
        -------
        np.ndarray
            A 4x4 geometric stiffness matrix for the truss element.
        """
        p = end_forces[2]
        l = self.length
        return p/l * np.array([[1, 0, -1, 0],
                         [0, 1, 0, -1],
                         [-1, 0, 1, 0],
                         [0, -1, 0, 1]])
