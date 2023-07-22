import numpy as np

from stableX.structure import Structure


class Solver:
    def __init__(self, structure: Structure):
        self.structure = structure
        self.degrees_of_freedom_count = len(self.structure.degrees_of_freedom)
        self._global_matrix = np.zeros((self.degrees_of_freedom_count, self.degrees_of_freedom_count))
        self._assemble_stiffness_matrix()
        self._displacement_vector = None
        self._force_vector = None

    def _assemble_stiffness_matrix(self):
        for element in self.structure.elements:
            i = 0
            for dof_i in element.stiffness_matrix_dofs:
                j = 0
                for dof_j in element.stiffness_matrix_dofs:
                    m = self.structure.degrees_of_freedom.index(dof_i)
                    n = self.structure.degrees_of_freedom.index(dof_j)
                    stiffness_term = element.global_stiffness_matrix()[i, j]
                    self._global_matrix[m, n] += stiffness_term
                    j += 1
                i += 1

    def _free_free_matrix(self):
        f = len(self.structure.free_degrees_of_freedom)
        return self._global_matrix[:f, :f]

    def _free_restrained_matrix(self):
        f = len(self.structure.free_degrees_of_freedom)
        return self._global_matrix[:f, f:]

    def _restrained_restrained_matrix(self):
        f = len(self.structure.free_degrees_of_freedom)
        return self._global_matrix[f:, f:]
    
    def _free_force_vector(self):
        return np.array([dof.force for dof in self.structure.free_degrees_of_freedom])

    def _restrained_displacement_vector(self):
        return np.array([dof.displacement for dof in self.structure.restrained_degrees_of_freedom])

    def solve_first_order_elastic(self):
        kff = self._free_free_matrix()
        kfs = self._free_restrained_matrix()
        kss = self._restrained_restrained_matrix()
        ff = self._free_force_vector()
        ds = self._restrained_displacement_vector()
        df = np.linalg.inv(kff).dot(ff - kfs.dot(ds))
        i = 0
        for dof in self.structure.free_degrees_of_freedom:
            dof.displacement = df[i]
            i += 1
        fs = kfs.T.dot(df) + kss.dot(ds)

    @property
    def force_vector(self):
        return self._force_vector

    @force_vector.setter
    def force_vector(self, value: np.ndarray):
        self._force_vector = value

    @property
    def displacement_vector(self):
        return self._displacement_vector

    @displacement_vector.setter
    def displacement_vector(self, value: np.ndarray):
        self._displacement_vector = value
