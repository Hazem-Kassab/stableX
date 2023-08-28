import numpy as np

from stableX.elements.unidimensional_elements.unidimensional_element import UniDimensionalElement


class TrussElement(UniDimensionalElement):
    def stiffness_matrix(self):
        e = self.elasticity_modulus
        a = self.section.area
        l = self.length

        return e*a/l*np.array([[1, -1],
                               [-1, 1]])

    def transformation_matrix(self):
        pass

    def shape_function(self, x):
        pass

    def b_matrix(self, x):
        pass

    def get_x_from_normal_coord(self, xi):
        pass

    def normal_b_matrix(self, xi):
        pass