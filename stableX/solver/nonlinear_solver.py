import numpy as np

from stableX.degree_of_freedom import DegreeOfFreedom
from stableX.solver.solver import Solver
from stableX.structure import Structure


class NonlinearSolver:

    def __init__(self, structure: Structure):
        self.structure = structure
        self.load = []
        self.displacement = []
        self.cumulative_displacement_vector = np.array([dof.displacement for dof
                                                        in self.structure.free_degrees_of_freedom], dtype='float64')

        self.cumulative_element_end_forces = [np.zeros(len(element.stiffness_matrix_dofs)) for element
                                              in self.structure.elements if element.geometric_nonlinearity]

        self.cumulative_element_global_end_forces = [np.zeros(len(element.stiffness_matrix_dofs)) for element
                                                     in self.structure.elements if element.geometric_nonlinearity]

    def solve_incrementally(self, number_of_steps: int, recorded_dof_load: DegreeOfFreedom,
                            recorded_dof: DegreeOfFreedom):
        solver = Solver(self.structure)
        step = 0
        cumulative_recorded_dof_displacement = 0
        solver.force_vector = solver.force_vector / number_of_steps
        while step <= number_of_steps:

            solver.solve_first_order_elastic()


            self.update_coordinates()

            self.cumulative_displacement_vector += solver.displacement_vector
            self.load.append(abs(recorded_dof_load.force * step))
            cumulative_recorded_dof_displacement += abs(recorded_dof.displacement)
            self.displacement.append(cumulative_recorded_dof_displacement)
            self.update_element_stiffness_matrix()
            step += 1

        solver.displacement_vector = self.cumulative_displacement_vector
        self.reset_node_coordinates()

    def update_coordinates(self):
        for node in self.structure.nodes:
            node.x += node.x_dof.displacement
            node.y += node.y_dof.displacement

    def reset_node_displacements(self):
        for node in self.structure.nodes:
            node.x -= node.x_dof.displacement
            node.y -= node.y_dof.displacement

    def reset_node_coordinates(self):
        for node in self.structure.nodes:
            node.x = node.x_original
            node.y = node.y_original

    def update_element_stiffness_matrix(self):
        counter = 0
        for element in self.structure.elements:
            if element.geometric_nonlinearity:
                self.cumulative_element_end_forces[counter] += element.end_forces()
                element_cum_forces = self.cumulative_element_end_forces[counter]
                element.stiffness_matrix = (element.first_order_elastic_stiffness_matrix()
                                            + element.geometric_stiffness_matrix(element_cum_forces))
                counter += 1

    def internal_force_vector(self):
        force = np.zeros(np.shape(self.structure.free_degrees_of_freedom))
        counter = 0
        for element in self.structure.elements:
            self.cumulative_element_global_end_forces[counter] += element.global_end_forces()
            dof_index = 0
            for dof in element.stiffness_matrix_dofs:
                if not dof.restrained:
                    index = self.structure.free_degrees_of_freedom.index(dof)
                    force[index] += self.cumulative_element_global_end_forces[counter][dof_index]
                dof_index += 1
            counter += 1
        return force

    # @property
    # def cumulative_displacement_vector(self):
    #     return self._cumulative_displacement_vector
    #
    # @cumulative_displacement_vector.setter
    # def cumulative_displacement_vector(self, value: np.ndarray):
    #     self._cumulative_displacement_vector = value
