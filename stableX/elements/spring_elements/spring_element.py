from abc import ABC

from stableX.elements.element import Element


class SpringElement(Element, ABC):

    def first_order_elastic_stiffness_matrix(self):
        pass

    def transformation_matrix(self):
        pass