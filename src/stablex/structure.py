from .elements.element import Element


class Structure:
    """
    Represents a structural system composed of multiple elements.

    Parameters
    ----------
    elements: list of Element
        Elements that define the structure.

    Attributes
    ----------
    elements : list of Element
        Elements that define the structure.
    """
    def __init__(self, elements: list[Element]):
        self.elements = elements

    @property
    def nodes(self):
        """
        Retrieve the unique set of nodes in the structure.

        Returns
        -------
        set of Node
            Set of nodes across all elements in the structure.
        """
        nodes = set()
        for element in self.elements:
            nodes = nodes.union(element.nodes)
        return nodes

    @property
    def degrees_of_freedom(self):
        """
        Retrieve the ordered list of all degrees of freedom in the structure.

        Returns
        -------
        list of DegreeOfFreedom
            Degrees of freedom sorted by restraint status and ID.
        """
        dofs = set()
        for element in self.elements:
            for dof in element.stiffness_matrix_dofs:
                dofs.add(dof)

        return sorted(dofs, key=lambda dof: (dof.restrained, dof.id))

    @property
    def free_degrees_of_freedom(self):
        """
        Retrieve the ordered list of free degrees of freedom in the structure.

        Returns
        -------
        list of DegreeOfFreedom
            Unrestrained degrees of freedom sorted by ID.
        """
        return sorted({dof for dof in self.degrees_of_freedom if not dof.restrained}, key=lambda dof: dof.id)

    @property
    def restrained_degrees_of_freedom(self):
        """
        Retrieve the ordered list of restrained degrees of freedom in the structure.

        Returns
        -------
        list of DegreeOfFreedom
            Restrained degrees of freedom sorted by ID.
        """
        return sorted({dof for dof in self.degrees_of_freedom if dof.restrained}, key=lambda dof: dof.id)
