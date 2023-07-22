from stableX.Elements.UniDimensionalElements.frame_element import FrameElement


class Structure:
    def __init__(self, elements: list[FrameElement]):
        self._elements = elements

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value: list[FrameElement]):
        self._elements = value

    @property
    def nodes(self):
        nodes = set()
        for element in self.elements:
            nodes = nodes.union(element.nodes)
        return nodes

    @property
    def degrees_of_freedom(self):
        dofs = set()
        for element in self.elements:
            for dof in element.stiffness_matrix_dofs:
                dofs.add(dof)

        return sorted(dofs, key=lambda dof: (dof.restrained, dof.id))

    @property
    def free_degrees_of_freedom(self):
        return sorted({dof for dof in self.degrees_of_freedom if not dof.restrained}, key=lambda dof: dof.id)

    @property
    def restrained_degrees_of_freedom(self):
        return sorted({dof for dof in self.degrees_of_freedom if dof.restrained}, key=lambda dof: dof.id)
