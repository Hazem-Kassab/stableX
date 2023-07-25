from abc import abstractmethod, ABC
from stableX import Node


class Element(ABC):

    def __init__(self, start_node: Node, end_node: Node):
        self._start_node = start_node
        self._end_node = end_node

    @property
    def nodes(self):
        return {self.start_node, self.end_node}

    @property
    @abstractmethod
    def stiffness_matrix_dofs(self):
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
    def stiffness_matrix(self):
        raise NotImplementedError

    def b_matrix(self, *args):
        raise NotImplementedError

    @abstractmethod
    def transformation_matrix(self):
        raise NotImplementedError

    def global_stiffness_matrix(self):
        return self.transformation_matrix().T.dot(self.stiffness_matrix()).dot(self.transformation_matrix())

