import numpy as np

from src.stablex.degree_of_freedom import DegreeOfFreedom
from src.stablex.solver.first_order_solver import Solver
from src.stablex.structure import Structure


class NonlinearSolver:
    """
    A class for solving nonlinear structural problems using an incremental approach.

    **Warning**: This solver is currently under development. It should not be used or should be used with caution,
    as it may undergo changes in future releases.

    Attributes:
        structure (Structure): The structure to be analyzed.
        load (list): A list to store applied loads at each step.
        displacement (list): A list to store cumulative displacements.
        cumulative_displacement_vector (np.array): A vector of cumulative displacements for free degrees of freedom.
        cumulative_element_end_forces (list): Cumulative end forces for elements with geometric nonlinearity.
        cumulative_element_global_end_forces (list): Cumulative global end forces for elements with geometric nonlinearity.
    """
    def __init__(self, structure: Structure):
        """
        Initializes the NonlinearSolver with a given structure.

        Args:
            structure (Structure): The structure to be solved.
        """
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
        """
         Solves the nonlinear problem incrementally over a specified number of steps.

         Args:
             number_of_steps (int): The number of increments to divide the load application.
             recorded_dof_load (DegreeOfFreedom): The degree of freedom associated with the load.
             recorded_dof (DegreeOfFreedom): The degree of freedom to record displacements for.
         """
        solver = Solver(self.structure)
        step = 0
        cumulative_recorded_dof_displacement = 0
        solver.force_vector = solver.force_vector / number_of_steps
        while step <= number_of_steps:
            self.update_element_stiffness_matrix()
            solver.solve_first_order_elastic()
            self.cumulative_displacement_vector += solver.displacement_vector
            self.load.append(abs(recorded_dof_load.force * step))
            cumulative_recorded_dof_displacement += abs(recorded_dof.displacement)
            self.displacement.append(cumulative_recorded_dof_displacement)
            self.update_coordinates()
            step += 1

        solver.displacement_vector = self.cumulative_displacement_vector
        self.reset_node_coordinates()

    def update_coordinates(self):
        """
        Updates the coordinates of all nodes in the structure based on their displacements.
        """
        for node in self.structure.nodes:
            node.x += node.x_dof.displacement
            node.y += node.y_dof.displacement

    def reset_node_coordinates(self):
        """
        Resets the coordinates of all nodes to their original values.
        """
        for node in self.structure.nodes:
            node.x = node._x_original
            node.y = node._y_original

    def update_element_stiffness_matrix(self):
        """
        Updates the stiffness matrix for all elements in the structure based on current displaced configuration and
        the current axial load.
        """
        counter = 0
        for element in self.structure.elements:
            if element.geometric_nonlinearity:
                self.cumulative_element_end_forces[counter] += element.local_end_forces()
                element_cum_forces = self.cumulative_element_end_forces[counter]
                element.stiffness_matrix = (element.first_order_elastic_stiffness_matrix()
                                            + element.geometric_stiffness_matrix(element_cum_forces))
                counter += 1
            else:
                element.stiffness_matrix = element.first_order_elastic_stiffness_matrix()

    def internal_force_vector(self):
        """
        Computes the internal force vector for the free degrees of freedom.

        Returns:
            np.array: The computed internal force vector.
        """
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
