import numpy as np

from stableX.degree_of_freedom import DegreeOfFreedom
from stableX.solver.solver import Solver
from stableX.structure import Structure


class EigenSolver:

    def __init__(self, structure: Structure):
        self.structure = structure

    def solve(self, mode_shape: int):
        self.reset_node_displacements()
        self.reset_node_coordinates()
        solver = Solver(self.structure)
        solver.solve_first_order_elastic()
        print(self.structure.elements[4].end_forces()[0])
        kff_matrix = solver._free_free_matrix(solver._global_stiffness_matrix)
        self.set_element_geometric_matrix()
        kffg_matrix = solver._free_free_matrix(solver._global_stiffness_matrix)
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(-kff_matrix).dot(kffg_matrix))
        eigenvalues = 1./eigenvalues
        eigenvectors = eigenvectors.T
        eigen_dict = EigenSolver.create_sorted_dict(eigenvalues, eigenvectors)
        mode_shape = mode_shape - 1
        eigenvalue = list(eigen_dict.keys())[mode_shape].real
        eigenvector = list(eigen_dict.values())[mode_shape]
        solver.displacement_vector = eigenvector

        return eigenvalue, eigenvectors

    def set_element_geometric_matrix(self):
        for element in self.structure.elements:
            if element.geometric_nonlinearity:
                element.stiffness_matrix = element.geometric_stiffness_matrix(element.end_forces())
            else:
                element.stiffness_matrix = element.geometric_stiffness_matrix(element.end_forces()*0)

    @staticmethod
    def create_sorted_dict(eigenvalues, eigenvectors):
        counter = 0
        eigen_dict = {}
        for value in eigenvalues:
            eigen_dict[value]= eigenvectors[counter]
            counter += 1
        sorted(eigen_dict)
        return dict(sorted(eigen_dict.items(), reverse=False))

    def reset_node_displacements(self):
        for node in self.structure.nodes:
            node.x_dof.displacement = 0
            node.y_dof.displacement = 0
            node.rz_dof.displacement = 0

    def reset_node_coordinates(self):
        for node in self.structure.nodes:
            node.x = node.x_original
            node.y = node.y_original


