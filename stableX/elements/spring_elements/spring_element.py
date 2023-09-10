from stableX.elements.element import Element


class SpringElement(Element):
    @property
    def stiffness_matrix_dofs(self) -> list:
        pass

    def first_order_elastic_stiffness_matrix(self):
        pass

    def geometric_stiffness_matrix(self):
        pass

    def transformation_matrix(self):
        pass