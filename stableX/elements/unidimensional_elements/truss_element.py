import numpy as np

from stableX.elements.unidimensional_elements.unidimensional_element import UniDimensionalElement


class TrussElement(UniDimensionalElement):
    @property
    def stiffness_matrix_dofs(self) -> list:
        return [self.start_node.x_dof, self.start_node.y_dof,
                self.end_node.x_dof, self.end_node.y_dof]

    def transformation_matrix(self):
        s = (self.end_node.y - self.start_node.y) / self.length
        c = (self.end_node.x - self.start_node.x) / self.length
        t = np.array([[c, s, 0, 0],
                      [-s, c, 0, 0],
                      [0, 0, c, s],
                      [0, 0, -s, c]])
        return t

    def shape_function(self, x):
        l = self.length
        return np.array([[1-x/l, 0, x/l, 0],
                         [0, 1-x/l, 0, x/l]])

    def b_matrix(self, x):
        pass

    def get_x_from_normal_coord(self, xi):
        pass

    def normal_b_matrix(self, xi):
        pass

    def first_order_elastic_stiffness_matrix(self):
        e = self.elasticity_modulus
        a = self.section.area
        l = self.length
        return e*a/l*np.array([[1, 0, -1, 0],
                               [0, 0, 0, 0],
                               [-1, 0, 1, 0],
                               [0, 0, 0, 0]])

    def geometric_stiffness_matrix(self, end_forces: np.ndarray):
        p = end_forces[2]
        l = self.length
        return p/l * np.array([[1, 0, -1, 0],
                         [0, 1, 0, -1],
                         [-1, 0, 1, 0],
                         [0, -1, 0, 1]])
