from stableX.Elements.frame_element import FrameElement


class Structure:
    def __init__(self, elements: list[FrameElement]):
        self.elements = elements
        self.free_dofs = set()
        self.restrained_dofs = set()
        self._get_free_and_restrained_dofs()

    def _get_free_and_restrained_dofs(self):
        for element in self.elements:
            for dof in element.dofs:
                if dof.restrained:
                    self.restrained_dofs.add(dof)
                else:
                    self.free_dofs.add(dof)
