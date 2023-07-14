from abc import ABC
from stableX.node import Node
from stableX.section import Section


class Element(ABC):
    id_counter = 1

    def __init__(self, start_node: Node, end_node: Node, section: Section, elasticity_modulus=1):
        self.id = Element.id_counter
        Element.id_counter += 1
        self._start_node = start_node
        self._end_node = end_node
        self._section = section
        self.elasticity_modulus = elasticity_modulus

    @property
    def nodes(self):
        return self.start_node, self.end_node

    @property
    def dofs(self):
        return [self.start_node.x_dof, self.start_node.y_dof, self.start_node.z_dof,
                self.end_node.x_dof, self.end_node.y_dof, self.end_node.z_dof]

    @property
    def start_node(self):
        return self._start_node

    @start_node.setter
    def start_node(self, value: Node):
        self._end_node = value

    @property
    def end_node(self):
        return self._end_node

    @end_node.setter
    def end_node(self, value: Node):
        self._end_node = value

    @property
    def length(self):
        return ((self.end_node.x - self.start_node.x) ** 2 +
                (self.end_node.y - self.start_node.y) ** 2) ** 0.5

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value: Section):
        self._section = value