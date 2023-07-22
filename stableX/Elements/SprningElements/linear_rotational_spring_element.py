import numpy as np

from stableX import Node
from stableX.Elements.element import Element


class LinearRotationalSpringElement(Element):

    def __init__(self, start_node: Node, end_node: Node, rotational_stiffness):
        super().__init__(start_node, end_node)
        self._rotational_stiffness = rotational_stiffness

    def stiffness_matrix(self):
        k = self.rotational_stiffness
        return k * np.array([[1, -1],
                             [-1, 1]])

    def transformation_matrix(self):
        return np.array([[1, 0],
                         [0, 1]])

    @property
    def rotational_stiffness(self):
        return self._rotational_stiffness

    @rotational_stiffness.setter
    def rotational_stiffness(self, value):
        self._rotational_stiffness = value

    @property
    def stiffness_matrix_dofs(self):
        return [self.start_node.rz_dof, self.end_node.rz_dof]
