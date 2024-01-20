from abc import abstractmethod, ABC

import numpy as np

from stableX import Node


class Element(ABC):
    id_counter = 1

    def __init__(self, start_node: Node, end_node: Node, include_geom_nonlinearity=False):
        self._start_node = start_node
        self._end_node = end_node
        self.geometric_nonlinearity = include_geom_nonlinearity
        # self.cumulative_end_forces = np.zeros(len(self.stiffness_matrix_dofs))
        self.id = Element.id_counter
        self.stiffness_matrix = np.zeros((len(self.stiffness_matrix_dofs), len(self.stiffness_matrix_dofs)))
        Element.id_counter += 1

    @property
    def nodes(self):
        return {self.start_node, self.end_node}

    @property
    @abstractmethod
    def stiffness_matrix_dofs(self) -> list:
        raise NotImplementedError

    @property
    def start_node(self) -> Node:
        return self._start_node

    @start_node.setter
    def start_node(self, value: Node):
        self._end_node = value

    @property
    def end_node(self) -> Node:
        return self._end_node

    @end_node.setter
    def end_node(self, value: Node):
        self._end_node = value

    @abstractmethod
    def first_order_elastic_stiffness_matrix(self):
        raise NotImplementedError

    @abstractmethod
    def geometric_stiffness_matrix(self, end_forces: np.ndarray):
        raise NotImplementedError

    @property
    def stiffness_matrix(self):
        return self._stiffness_matrix

    @stiffness_matrix.setter
    def stiffness_matrix(self, value: np.ndarray):
        self._stiffness_matrix = value

    def b_matrix(self, *args):
        raise NotImplementedError

    @abstractmethod
    def transformation_matrix(self):
        raise NotImplementedError

    def global_stiffness_matrix(self):
        return self.transformation_matrix().T.dot(self.stiffness_matrix).dot(self.transformation_matrix())

    # @property
    # def cumulative_end_forces(self):
    #     return self._cumulative_end_forces
    #
    # @cumulative_end_forces.setter
    # def cumulative_end_forces(self, value: np.ndarray):
    #     self._cumulative_end_forces = value

    def global_end_displacements(self):
        return np.array([dof.displacement for dof in self.stiffness_matrix_dofs])

    def local_end_displacements(self):
        return self.transformation_matrix().dot(self.global_end_displacements())

    def end_forces(self):
        return self.stiffness_matrix.dot(self.local_end_displacements())

    def global_end_forces(self):
        return self.global_stiffness_matrix().dot(self.global_end_displacements())
