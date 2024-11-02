import numpy as np

from src.stablex.structure import Structure


class Solver:
    """
    Solver class to perform structural analysis on a given structure by calculating displacements
    and reaction forces based on the first-order elastic stiffness matrix.

    Parameters
    ----------
    structure : Structure
        The structure to analyze.
    """
    def __init__(self, structure: Structure):
        self.structure = structure
        self.degrees_of_freedom_count = len(self.structure.degrees_of_freedom)
        self._force_vector = np.array([dof.force for dof in self.structure.free_degrees_of_freedom])
        self._displacement_vector = np.zeros(len(structure.free_degrees_of_freedom))
        self._reactions_vector = np.zeros(len(structure.restrained_degrees_of_freedom))
        for element in structure.elements:
            element.stiffness_matrix = element.first_order_elastic_stiffness_matrix()

    @property
    def _global_stiffness_matrix(self):
        """
        Constructs the global stiffness matrix for the entire structure.

        Returns
        -------
        np.ndarray
            The global stiffness matrix.
        """
        global_matrix = np.zeros((self.degrees_of_freedom_count, self.degrees_of_freedom_count))
        for element in self.structure.elements:
            element_stiffness_matrix = element.global_stiffness_matrix()
            i = 0
            for dof_i in element.stiffness_matrix_dofs:
                j = 0
                for dof_j in element.stiffness_matrix_dofs:
                    m = self.structure.degrees_of_freedom.index(dof_i)
                    n = self.structure.degrees_of_freedom.index(dof_j)
                    stiffness_term = element_stiffness_matrix[i, j]
                    global_matrix[m, n] += stiffness_term
                    j += 1
                i += 1

        return global_matrix

    def _free_free_matrix(self, global_matrix: np.ndarray):
        """
        Extracts the free-free partition from the global stiffness matrix.

        Parameters
        ----------
        global_matrix : np.ndarray
            The global stiffness matrix.

        Returns
        -------
        np.ndarray
            The free-free partition of the stiffness matrix.
        """
        f = len(self.structure.free_degrees_of_freedom)
        return global_matrix[:f, :f]

    def _free_restrained_matrix(self, global_matrix: np.ndarray):
        """
        Extracts the free-restrained partition from the global stiffness matrix.

        Parameters
        ----------
        global_matrix : np.ndarray
            The global stiffness matrix.

        Returns
        -------
        np.ndarray
            The free-restrained partition of the stiffness matrix.
        """
        f = len(self.structure.free_degrees_of_freedom)
        return global_matrix[:f, f:]

    def _restrained_restrained_matrix(self, global_matrix: np.ndarray):
        """
        Extracts the restrained-restrained partition from the global stiffness matrix.

        Parameters
        ----------
        global_matrix : np.ndarray
            The global stiffness matrix.

        Returns
        -------
        np.ndarray
            The restrained-restrained partition of the stiffness matrix.
        """
        f = len(self.structure.free_degrees_of_freedom)
        return global_matrix[f:, f:]

    def _restrained_displacement_vector(self):
        """
        Retrieves the displacement values of the restrained degrees of freedom.

        Returns
        -------
        np.ndarray
            The displacement vector for restrained degrees of freedom.
        """
        return np.array([dof.displacement for dof in self.structure.restrained_degrees_of_freedom])

    def solve_first_order_elastic(self):
        """
        Solves for displacements and reaction forces using first-order elastic stiffness analysis.
        """
        global_matrix = self._global_stiffness_matrix
        kff = self._free_free_matrix(global_matrix)
        kfs = self._free_restrained_matrix(global_matrix)
        kss = self._restrained_restrained_matrix(global_matrix)
        ff = self.force_vector
        ds = self._restrained_displacement_vector()
        self.displacement_vector = np.linalg.inv(kff).dot(ff - kfs.dot(ds))
        self.reactions_vector = kfs.T.dot(self.displacement_vector) + kss.dot(ds)

    @property
    def force_vector(self) -> np.ndarray:
        """
        Gets the force vector for the structure.

        Returns
        -------
        np.ndarray
            The force vector applied to the structure.
        """
        return self._force_vector

    @force_vector.setter
    def force_vector(self, value: np.ndarray):
        """
        Sets the force vector for free degrees of freedom.

        Parameters
        ----------
        value : np.ndarray
            New force values for the free degrees of freedom, updating the associated DOFs in the structure.
        """
        i = 0
        for dof in self.structure.free_degrees_of_freedom:
            dof.force = value[i]
            i += 1
        self._force_vector = value

    @property
    def displacement_vector(self):
        """
        Gets the displacement vector for free degrees of freedom.

        Returns
        -------
        np.ndarray
            The displacement vector for free degrees of freedom.
        """
        return self._displacement_vector

    @displacement_vector.setter
    def displacement_vector(self, value: np.ndarray):
        """
        Gets the reaction forces vector for restrained degrees of freedom.

        Returns
        -------
        np.ndarray
            The reactions vector for restrained degrees of freedom.
        """
        i = 0
        for dof in self.structure.free_degrees_of_freedom:
            dof.displacement = value[i]
            i += 1
        self._displacement_vector = value

    @property
    def reactions_vector(self):
        """
        Gets the reaction forces vector for restrained degrees of freedom.

        Returns
        -------
        np.ndarray
            The reactions vector for restrained degrees of freedom.
        """
        return self._reactions_vector

    @reactions_vector.setter
    def reactions_vector(self, value: np.ndarray):
        """
        Sets the reaction forces vector for restrained degrees of freedom.

        Parameters
        ----------
        value : np.ndarray
             Reaction values for the restrained degrees of freedom, updating the associated DOFs in the structure.
        """
        i = 0
        for dof in self.structure.restrained_degrees_of_freedom:
            dof.force = value[i]
            i += 1
        self._reactions_vector = value
