import math
import numpy as np
from stableX.Elements.element import Element
from stableX.stability_functions import *


class FrameElement(Element):
    id_counter = 1

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
