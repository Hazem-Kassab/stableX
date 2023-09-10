import math
import numpy as np
from stableX.elements.unidimensional_elements.unidimensional_element import UniDimensionalElement
from stableX.stability_functions import *


class FrameElement(UniDimensionalElement):

    @property
    def stiffness_matrix_dofs(self) -> list:
        return [self.start_node.x_dof, self.start_node.y_dof, self.start_node.rz_dof,
                self.end_node.x_dof, self.end_node.y_dof, self.end_node.rz_dof]

    @property
    def euler_load(self):
        return math.pi**2 * self.elasticity_modulus * self.section.inertia/self.length**2

    def stability_stiffness_matrix(self, load):
        r = self.section.radius_of_gyration
        l = self.length
        e = self.elasticity_modulus
        i = self.section.inertia
        k = e * l / i
        ul = math.pi * math.sqrt(load/self.euler_load)
        return k * np.array([[1/(r**2),               0,            0,   -1/(r**2),             0,             0],
                             [0,            ss(ul)/l**2,    -sb(ul)/l,           0,  -ss(ul)/l**2,     -sb(ul)/l],
                             [0,              -sb(ul)/l,        s(ul),           0,      sb(ul)/l,   s(ul)*c(ul)],
                             [-1/(r**2),              0,            0,    1/(r**2),             0,             0],
                             [0,           -ss(ul)/l**2,     sb(ul)/l,           0,   ss(ul)/l**2,      sb(ul)/l],
                             [0,              -sb(ul)/l,  s(ul)*c(ul),           0,      sb(ul)/l,        s(ul)]])

    def first_order_elastic_stiffness_matrix(self):
        e = self.elasticity_modulus
        i = self.section.inertia
        l = self.length
        a = self.section.area

        return np.array([[a*e/l,        0,           0, -a*e/l,            0,           0],
                         [0,  12*e*i/l**3,  6*e*i/l**2,      0, -12*e*i/l**3,  6*e*i/l**2],
                         [0,   6*e*i/l**2,     4*e*i/l,      0,  -6*e*i/l**2,     2*e*i/l],
                         [-a*e/l,       0,           0,  a*e/l,            0,           0],
                         [0, -12*e*i/l**3, -6*e*i/l**2,      0,  12*e*i/l**3, -6*e*i/l**2],
                         [0,   6*e*i/l**2,     2*e*i/l,      0,  -6*e*i/l**2,     4*e*i/l]])

    def geometric_stiffness_matrix(self):
        l = self.length
        p = self.cumulative_end_forces[3]
        # print(self.euler_load)
        return p/l * np.array([[1,    0,         0, -1,     0,         0],
                               [0,  6/5,      l/10,  0,  -6/5,      l/10],
                               [0, l/10, 2*l**2/15,  0, -l/10,  -l**2/30],
                               [-1,   0,         0,  1,     0,         0],
                               [0, -6/5,     -l/10,  0,   6/5,     -l/10],
                               [0, l/10,  -l**2/30,  0, -l/10, 2*l**2/15]])

    def shape_function(self, x):
        l = self.length
        return np.array([[1-x/l, 0, 0, x/l, 0, 0],
                         [0, 1-3*x**2/l**2 + 2*x**3/l**3, x-2*x**2/l + x**3/l**2, 0,
                          3*x**2/l**2 - 2*x**3/l**3, -x**2/l + x**3/l**2]])

    def b_matrix(self, x):
        l = self.length
        e = self.elasticity_modulus
        a = self.section.area
        i = self.section.inertia
        return np.array([np.array([-1/l, 0, 0, 1/l, 0, 0])*sqrt(e*a),
                        np.array([0, 12*x/l**3 - 6/l**2, 6*x/l**2 - 4/l, 0, 6/l**2 - 12*x/l**3, 6*x/l**2 - 2/l])*sqrt(e*i)])

    def get_x_from_normal_coord(self, xi):
        return self.length/2 * (xi+1)

    def normal_b_matrix(self, xi):
        x = self.get_x_from_normal_coord(xi)
        return self.b_matrix(x)

    def stiffness_matrix_2(self):
        xi = 1/sqrt(3)
        return self.length/2 * (np.dot(self.normal_b_matrix(xi).T, self.normal_b_matrix(xi)) +
                              np.dot(self.normal_b_matrix(-xi).T, self.normal_b_matrix(-xi)))

    def transformation_matrix(self):
        s = (self.end_node.y - self.start_node.y)/self.length
        c = (self.end_node.x - self.start_node.x)/self.length
        t = np.array([[c,  s, 0],
                      [-s, c, 0],
                      [0,  0, 1]])
        transformation_matrix = np.zeros((6, 6))
        transformation_matrix[:3, :3] = t
        transformation_matrix[3:, 3:] = t
        return transformation_matrix

