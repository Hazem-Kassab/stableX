import math
import numpy as np
from stablex.elements.unidimensional_elements.unidimensional_element import UniDimensionalElement
from stablex.stability_functions import *
from stablex.degree_of_freedom import DegreeOfFreedom


class FrameElement(UniDimensionalElement):
    """
    Represents a frame element in a structural analysis model. A frame element can resist axial,
    shear, and bending forces, supporting deformation in both translational and rotational degrees
    of freedom.

    Attributes
    ----------
    start_node : Node
        The starting node of the frame element.
    end_node : Node
        The ending node of the frame element.
    section : Section
        The cross-sectional properties of the element.
    geometric_nonlinearity : bool
        Whether geometric nonlinearity is included in the element.
    elasticity_modulus : float
        The modulus of elasticity for the frame element material.

    Methods
    -------
    stiffness_matrix_dofs() -> list[DegreeOfFreedom]
        Returns the list of degrees of freedom relevant to the frame element's stiffness matrix.
    euler_load() -> float
        Calculates the Euler load for the frame element based on material and section properties.
    stability_stiffness_matrix(load: float) -> np.ndarray
        Computes the stability stiffness matrix based on the applied load.
    first_order_elastic_stiffness_matrix() -> np.ndarray
        Computes the first-order elastic stiffness matrix for the frame element.
    geometric_stiffness_matrix(end_forces: np.ndarray) -> np.ndarray
        Returns the geometric stiffness matrix for the element, based on the end forces.
    shape_function(x: float) -> np.ndarray
        Calculates the shape function at a specified local coordinate.
    b_matrix(x: float) -> np.ndarray
        Computes the strain-displacement matrix (B-matrix) at a specified local coordinate.
    get_x_from_normal_coord(xi: float) -> float
        Converts a normalized coordinate to the actual x-coordinate along the element.
    normal_b_matrix(xi: float) -> np.ndarray
        Computes the strain-displacement matrix for a given normalized coordinate.
    stiffness_matrix_2() -> np.ndarray
        Computes an alternate stiffness matrix using Gaussian quadrature for accuracy.
    transformation_matrix() -> np.ndarray
        Computes the transformation matrix to align the local and global coordinate systems.
    """

    @property
    def stiffness_matrix_dofs(self) -> list[DegreeOfFreedom]:
        """
        Returns the degrees of freedom for the frame element's stiffness matrix.

        Returns
        -------
        list[DegreeOfFreedom]
            A list of degrees of freedom objects, ordered as [start_node.x_dof, start_node.y_dof,
            start_node.rz_dof, end_node.x_dof, end_node.y_dof, end_node.rz_dof].
        """
        return [self.start_node.x_dof, self.start_node.y_dof, self.start_node.rz_dof,
                self.end_node.x_dof, self.end_node.y_dof, self.end_node.rz_dof]

    @property
    def euler_load(self):
        """
        Calculates the Euler load, representing the critical buckling load for the frame element.

        Returns
        -------
        float
            The Euler load for the frame element.
        """
        return math.pi**2 * self.elasticity_modulus * self.section.inertia/self.length**2

    def stability_stiffness_matrix(self, load):
        """
        Calculates the stiffness matrix using stability functions, based on the internal axial force.

        Note
        ----
        This method is currently not utilized in the analysis process. It may be integrated as a feature in future releases.

        Parameters
        ----------
        load : float
            The axial load applied to the element.

        Returns
        -------
        np.ndarray
            A 6x6 stability stiffness matrix.
        """
        r = self.section.radius_of_gyration
        l = self.length
        e = self.elasticity_modulus
        i = self.section.inertia
        k = e * l / i
        ul = math.pi * math.sqrt(load/self.euler_load)
        return k * np.array([[1/(r**2),               0,            0,   -1/(r**2),             0,             0],
                             [0,            ss(ul)/l**2,    -sb(ul)/l,           0,  -ss(ul)/l**2,     -sb(ul)/l],
                             [0,              -sb(ul)/l,        s(ul),           0,      sb(ul)/l,   s(ul)*c(ul)],
                             [-1/(r**2),              0,            0,    1/(r**2),             0,             0],
                             [0,           -ss(ul)/l**2,     sb(ul)/l,           0,   ss(ul)/l**2,      sb(ul)/l],
                             [0,              -sb(ul)/l,  s(ul)*c(ul),           0,      sb(ul)/l,        s(ul)]])

    def first_order_elastic_stiffness_matrix(self):
        """
        Calculates the first-order elastic stiffness matrix for the frame element, based on its
        section properties and elasticity modulus.

        Returns
        -------
        np.ndarray
            A 6x6 elastic stiffness matrix for the frame element.
        """
        e = self.elasticity_modulus
        i = self.section.inertia
        l = self.length
        a = self.section.area
        return np.array([[a*e/l,        0,           0, -a*e/l,            0,           0],
                         [0,  12*e*i/l**3,  6*e*i/l**2,      0, -12*e*i/l**3,  6*e*i/l**2],
                         [0,   6*e*i/l**2,     4*e*i/l,      0,  -6*e*i/l**2,     2*e*i/l],
                         [-a*e/l,       0,           0,  a*e/l,            0,           0],
                         [0, -12*e*i/l**3, -6*e*i/l**2,      0,  12*e*i/l**3, -6*e*i/l**2],
                         [0,   6*e*i/l**2,     2*e*i/l,      0,  -6*e*i/l**2,     4*e*i/l]])

    def geometric_stiffness_matrix(self, end_forces: np.ndarray):
        """
        Computes the geometric stiffness matrix based on end forces.

        Parameters
        ----------
        end_forces : np.ndarray
            A vector of end forces, where end_forces[3] represents the axial force.

        Returns
        -------
        np.ndarray
            A 6x6 geometric stiffness matrix.
        """
        l = self.length
        p = end_forces[3]
        return p/l * np.array([[1,    0,         0, -1,     0,         0],
                               [0,  6/5,      l/10,  0,  -6/5,      l/10],
                               [0, l/10, 2*l**2/15,  0, -l/10,  -l**2/30],
                               [-1,   0,         0,  1,     0,         0],
                               [0, -6/5,     -l/10,  0,   6/5,     -l/10],
                               [0, l/10,  -l**2/30,  0, -l/10, 2*l**2/15]])

    def shape_function(self, x):
        """
        Calculates the shape function for a specified local coordinate along the frame element.

        Parameters
        ----------
        x : float
            The local coordinate along the length of the element.

        Returns
        -------
        np.ndarray
            A 2x6 array representing the shape functions.
        """
        l = self.length
        return np.array([[1-x/l, 0, 0, x/l, 0, 0],
                         [0, 1-3*x**2/l**2 + 2*x**3/l**3, x-2*x**2/l + x**3/l**2, 0,
                          3*x**2/l**2 - 2*x**3/l**3, -x**2/l + x**3/l**2]])

    def b_matrix(self, x):
        """
        Computes the strain-displacement matrix (B-matrix) for a specified local coordinate.

        Parameters
        ----------
        x : float
            The local coordinate along the element's length.

        Returns
        -------
        np.ndarray
            The B-matrix, which relates strains to displacements.
        """
        l = self.length
        e = self.elasticity_modulus
        a = self.section.area
        i = self.section.inertia
        return np.array([np.array([-1/l, 0, 0, 1/l, 0, 0])*sqrt(e*a),
                        np.array([0, 12*x/l**3 - 6/l**2, 6*x/l**2 - 4/l, 0, 6/l**2 - 12*x/l**3, 6*x/l**2 - 2/l])*sqrt(e*i)])

    def get_x_from_normal_coord(self, xi):
        """
        Converts a normalized coordinate to the actual x-coordinate along the element.

        Parameters
        ----------
        xi : float
            A normalized coordinate within [-1, 1].

        Returns
        -------
        float
            The physical x-coordinate corresponding to the normalized coordinate.
        """
        return self.length/2 * (xi+1)

    def normal_b_matrix(self, xi):
        """
        Computes the B-matrix for a given normalized coordinate, used for integration.

        Parameters
        ----------
        xi : float
            The normalized coordinate within [-1, 1].

        Returns
        -------
        np.ndarray
            The strain-displacement matrix at the given normalized coordinate.
        """
        x = self.get_x_from_normal_coord(xi)
        return self.b_matrix(x)

    def stiffness_matrix_2(self):
        """
        Computes an alternate stiffness matrix using Gaussian quadrature.

        Note
        ----
        This method is currently not utilized in the analysis process. It may be integrated as a feature in future releases.

        Returns
        -------
        np.ndarray
            A stiffness matrix computed using Gaussian quadrature for enhanced accuracy.
        """
        xi = 1/sqrt(3)
        return self.length/2 * (np.dot(self.normal_b_matrix(xi).T, self.normal_b_matrix(xi)) +
                              np.dot(self.normal_b_matrix(-xi).T, self.normal_b_matrix(-xi)))

    def transformation_matrix(self):
        """
        Computes the transformation matrix that aligns the element's local coordinates with the
        global coordinate system.

        Returns
        -------
        np.ndarray
            A 6x6 transformation matrix.
        """
        s = (self.end_node.y - self.start_node.y)/self.length
        c = (self.end_node.x - self.start_node.x)/self.length
        t = np.array([[c,  s, 0],
                      [-s, c, 0],
                      [0,  0, 1]])
        transformation_matrix = np.zeros((6, 6))
        transformation_matrix[:3, :3] = t
        transformation_matrix[3:, 3:] = t
        return transformation_matrix
