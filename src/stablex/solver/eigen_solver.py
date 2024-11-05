import numpy as np

from stablex.solver.first_order_solver import Solver
from stablex.structure import Structure


class EigenSolver:

    """
    Performs buckling analysis for the structure to determine the critical buckling load and the corresponding buckling mode.

    Methods
    -------
    solve(mode_shape: int)
        Solves for the specified buckling mode, returning the critical load factor (eigenvalue) and mode shape (eigenvector).
    set_element_geometric_matrix()
        Sets the geometric stiffness matrix for each element in the structure.
    create_sorted_dict(eigenvalues, eigenvectors)
        Creates and returns a sorted dictionary of eigenvalues and their corresponding eigenvectors.
    reset_node_displacements()
        Resets the displacements of all nodes' degrees of freedom to zero.
    reset_node_coordinates()
        Resets each node's coordinates to its original position.
    """

    def __init__(self, structure: Structure):
        """
        Initializes the EigenSolver with a structural model to perform buckling analysis.

        Parameters
        ----------
        structure : Structure
            The structural model for which to perform the buckling analysis.
        """
        self.structure = structure

    def solve(self, mode_shape: int):
        """
        Performs a buckling analysis by first executing a first-order elastic analysis to determine
        the axial loads in the structural members, then solving for the eigenvalues and eigenvectors
        of the buckling equation:

            (-[K_E]⁻¹[K_g] - λ[I]){Δ} = 0

        where:
        - **[K_E]** is the elastic stiffness matrix from the first-order analysis,
        - **[K_g]** is the geometric stiffness matrix based on the internal axial forces,
        - **λ** represents the eigenvalues associated with critical buckling loads,
        - **[I]** is the identity matrix, and
        - **{Δ}** is the eigenvector representing the buckling mode shape.

        The eigenvalues obtained represent the load factors at which buckling occurs,
        and the corresponding eigenvectors indicate the buckling mode shapes.

        Parameters
        ----------
        mode_shape : int
            The mode shape number for which to solve.

        Returns
        -------
        tuple
            A tuple containing the selected eigenvalue and eigenvectors for the specified mode shape.
        """
        self.reset_node_displacements()
        self.reset_node_coordinates()
        solver = Solver(self.structure)
        solver.solve_first_order_elastic()
        kff_matrix = solver._free_free_matrix(solver._global_stiffness_matrix)
        self.reset_node_coordinates()
        self.set_element_geometric_matrix()
        kffg_matrix = solver._free_free_matrix(solver._global_stiffness_matrix)
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(-kff_matrix).dot(kffg_matrix))
        eigen_dict = EigenSolver.create_sorted_dict(1./eigenvalues, eigenvectors.T)
        eigenvalue = list(eigen_dict.keys())[mode_shape-1].real
        eigenvector = list(eigen_dict.values())[mode_shape-1]
        solver.displacement_vector = eigenvector

        return eigenvalue, eigenvectors

    def set_element_geometric_matrix(self):
        """
         Sets the geometric stiffness matrix for each element in the structure, accounting for nonlinearity.
         """
        for element in self.structure.elements:
            if element.geometric_nonlinearity:
                element.stiffness_matrix = element.geometric_stiffness_matrix(element.local_end_forces())
            else:
                element.stiffness_matrix = element.geometric_stiffness_matrix(element.local_end_forces() * 0)

    @staticmethod
    def create_sorted_dict(eigenvalues, eigenvectors):
        """
        Creates a sorted dictionary of eigenvalues and corresponding eigenvectors.

        Parameters
        ----------
        eigenvalues : array-like
            Eigenvalues to be sorted.
        eigenvectors : array-like
            Corresponding eigenvectors for each eigenvalue.

        Returns
        -------
        dict
            A dictionary mapping each eigenvalue to its eigenvector, sorted in ascending order of eigenvalues.
        """
        counter = 0
        eigen_dict = {}
        for value in eigenvalues:
            eigen_dict[value]= eigenvectors[counter]
            counter += 1
        sorted(eigen_dict)
        return dict(sorted(eigen_dict.items(), reverse=False))

    def reset_node_displacements(self):
        """
        Resets displacements of all degrees of freedom in each node to zero.
        """
        for node in self.structure.nodes:
            node.x_dof.displacement = 0
            node.y_dof.displacement = 0
            node.rz_dof.displacement = 0

    def reset_node_coordinates(self):
        """
        Resets coordinates of each node to its original position.
        """
        for node in self.structure.nodes:
            node.x = node._x_original
            node.y = node._y_original
