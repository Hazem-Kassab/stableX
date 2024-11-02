class DegreeOfFreedom:
    """
    Internal class representing a degree of freedom

    This class is used internally by node objects. Each node object instantiates
    three degree of freedom objects; two translational and one rotational.

    Attributes
    ----------
    id : int
        A unique identifier for the degree of freedom.
    displacement : float
        The displacement value associated with the degree of freedom.
        This value is determined after analysis and defaults to 0.0.

    Properties
    ----------
    restrained : Boolean
        A flag indicating whether the degree of freedom is restrained (boundary condition applied).
        The default value is False
    force : float
        Used to assign a nodal force to a node in the direction of the degree of freedom.

    """

    id_counter = 1

    def __init__(self):
        """
        Initializes the DegreeOfFreedom with default values.

        The degree of freedom is initialized with default attributes:
        - restrained: False
        - displacement: 0.0
        - force: 0.0
        """
        self.id = DegreeOfFreedom.id_counter
        self._restrained = False
        self.displacement = 0
        DegreeOfFreedom.id_counter += 1
        self._force = 0

    @property
    def restrained(self) -> bool:
        """Gets the boundary condition of the degree of freedom."""
        return self._restrained

    @restrained.setter
    def restrained(self, value: bool):
        """Sets the boundary condition of the degree of freedom.

        Parameters
        ----------
        value : bool
            Indicates whether the degree of freedom should be restrained.
        """
        self._restrained = value

    @property
    def force(self) -> float:
        """Gets the force applied at the node in the direction of the degree of freedom."""
        return self._force

    @force.setter
    def force(self, value: float):
        """Applies a force at the node in the direction of the degree of freedom."""
        self._force = value
