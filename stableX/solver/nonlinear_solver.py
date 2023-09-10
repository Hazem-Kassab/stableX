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

    def solve_incrementally(self, number_of_steps: int, recorded_dof_load: DegreeOfFreedom, recorded_dof: DegreeOfFreedom):
        solver = Solver(self.structure)
        step = 0
        force_vector = solver.force_vector/number_of_steps
        while step <= number_of_steps:
            solver.force_vector = force_vector
            solver.solve_first_order_elastic()
            self.update_element_end_forces()
            self.update_coordinates()
            self.cumulative_displacement_vector += solver.displacement_vector
            self.load.append(abs(recorded_dof_load.force*step))
            self.displacement.append(abs(recorded_dof.displacement))
            step += 1

        solver.displacement_vector = self.cumulative_displacement_vector
        self.reset_node_coordinates()

    def update_coordinates(self):
        for node in self.structure.nodes:
            node.x += node.x_dof.displacement
            node.y += node.y_dof.displacement

    def reset_node_coordinates(self):
        for node in self.structure.nodes:
            node.x = node.x_original
            node.y = node.y_original

    def update_element_end_forces(self):
        for element in self.structure.elements:
            # print(element.id)
            # print(element.cumulative_end_forces)
            element.cumulative_end_forces += element.end_forces()

    @property
    def cumulative_displacement_vector(self):
        return self._cumulative_displacement_vector

    @cumulative_displacement_vector.setter
    def cumulative_displacement_vector(self, value: np.ndarray):
        self._cumulative_displacement_vector = value
