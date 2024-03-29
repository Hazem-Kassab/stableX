from abc import ABC, abstractmethod
import numpy as np
from stableX.elements.element import Element
from stableX.node import Node
from stableX.section import Section


class UniDimensionalElement(Element, ABC):

    def __init__(self, start_node: Node, end_node: Node, section: Section, include_geom_nonlinearity=False, elasticity_modulus=200000):
        super().__init__(start_node, end_node, include_geom_nonlinearity)
        self._start_node = start_node
        self._end_node = end_node
        self._section = section
        self.elasticity_modulus = elasticity_modulus

    @property
    def length(self):
        return ((self.end_node.x - self.start_node.x) ** 2 +
                (self.end_node.y - self.start_node.y) ** 2) ** 0.5

    @property
    def section(self) -> Section:
        return self._section

    @section.setter
    def section(self, value: Section):
        self._section = value

    @abstractmethod
    def transformation_matrix(self):
        raise NotImplementedError

    @abstractmethod
    def shape_function(self, x):
        raise NotImplementedError

    @abstractmethod
    def b_matrix(self, x):
        raise NotImplementedError

    @abstractmethod
    def get_x_from_normal_coord(self, xi):
        raise NotImplementedError

    @abstractmethod
    def normal_b_matrix(self, xi):
        raise NotImplementedError

    @abstractmethod
    def stiffness_matrix_dofs(self) -> list:
        pass

    def get_local_displacement(self, x):
        return self.shape_function(x).dot(self.local_end_displacements())
