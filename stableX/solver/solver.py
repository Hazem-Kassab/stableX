import numpy as np

from stableX.structure import Structure


class Solver:
    def __init__(self, structure: Structure):
        self.structure = structure
        self.degrees_of_freedom_count = len(self.structure.degrees_of_freedom)
        self.force_vector = np.array([dof.force for dof in self.structure.free_degrees_of_freedom])
        self.displacement_vector = np.array([dof.displacement for dof in self.structure.free_degrees_of_freedom])
        self.reactions_vector = np.array([dof.force for dof in self.structure.restrained_degrees_of_freedom])

    def _assemble_stiffness_matrix(self):
        global_matrix = np.zeros((self.degrees_of_freedom_count, self.degrees_of_freedom_count))
        for element in self.structure.elements:
            i = 0
            for dof_i in element.stiffness_matrix_dofs:
                j = 0
                for dof_j in element.stiffness_matrix_dofs:
                    m = self.structure.degrees_of_freedom.index(dof_i)
                    n = self.structure.degrees_of_freedom.index(dof_j)
                    stiffness_term = element.global_stiffness_matrix()[i, j]
                    global_matrix[m, n] += stiffness_term
                    j += 1
                i += 1

        return global_matrix

    def _free_free_matrix(self, global_matrix: np.ndarray):
        f = len(self.structure.free_degrees_of_freedom)
        return global_matrix[:f, :f]

    def _free_restrained_matrix(self, global_matrix: np.ndarray):
        f = len(self.structure.free_degrees_of_freedom)
        return global_matrix[:f, f:]

    def _restrained_restrained_matrix(self, global_matrix: np.ndarray):
        f = len(self.structure.free_degrees_of_freedom)
        return global_matrix[f:, f:]
    
    # def _free_force_vector(self):
    #     self.force_vector = np.array([dof.force for dof in self.structure.free_degrees_of_freedom])

    def _restrained_displacement_vector(self):
        return np.array([dof.displacement for dof in self.structure.restrained_degrees_of_freedom])

    def solve_first_order_elastic(self):
        global_matrix = self._assemble_stiffness_matrix()
        kff = self._free_free_matrix(global_matrix)
        # print(kff[0, 0])
        kfs = self._free_restrained_matrix(global_matrix)
        kss = self._restrained_restrained_matrix(global_matrix)
        ff = self.force_vector
        ds = self._restrained_displacement_vector()
        self.displacement_vector = np.linalg.inv(kff).dot(ff - kfs.dot(ds))
        self.reactions_vector = kfs.T.dot(self.displacement_vector) + kss.dot(ds)

    @property
    def force_vector(self):
        return self._force_vector

    @force_vector.setter
    def force_vector(self, value: np.ndarray):
        i = 0
        for dof in self.structure.free_degrees_of_freedom:
            dof.force = value[i]
            i += 1
        self._force_vector = value

    @property
    def displacement_vector(self):
        return self._displacement_vector

    @displacement_vector.setter
    def displacement_vector(self, value: np.ndarray):
        i = 0
        for dof in self.structure.free_degrees_of_freedom:
            dof.displacement = value[i]
            i += 1
        self._displacement_vector = value

    @property
    def reactions_vector(self):
        return self._reactions_vector

    @reactions_vector.setter
    def reactions_vector(self, value: np.ndarray):
        i = 0
        for dof in self.structure.restrained_degrees_of_freedom:
            dof.force = value[i]
            i += 1
        self._reactions_vector = value




