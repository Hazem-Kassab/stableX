from stableX.elements.unidimensional_elements.unidimensional_element import UniDimensionalElement


class UniDimensionalElementSubClass(UniDimensionalElement):
    def first_order_elastic_stiffness_matrix(self):
        pass

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