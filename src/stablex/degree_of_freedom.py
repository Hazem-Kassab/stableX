class DegreeOfFreedom:
    """
    Internal class representing a degree of freedom

    This class is used internally by node objects. Each node object instantiates
    three degree of freedom objects; two translational and one rotational.

    Attributes
    ----------
    id : int
        A unique identifier for the degree of freedom.
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
        self._displacement = 0
        DegreeOfFreedom.id_counter += 1
        self._force = 0

    @property
    def displacement(self) -> float:
        """
        Gets and sets the displacement of the node in the direction of the degree of freedom.
        Initialized with value 0.0.
        """
        return self._displacement

    @displacement.setter
    def displacement(self, value: float):
        self._displacement = value

    @property
    def restrained(self) -> bool:
        """
        Gets and sets the boundary condition of the node in the direction of the degree of freedom.
        False by default.
        """
        return self._restrained

    @restrained.setter
    def restrained(self, value: bool):
        self._restrained = value

    @property
    def force(self) -> float:
        """Gets and sets the force applied at the node in the direction of the degree of freedom."""
        return self._force

    @force.setter
    def force(self, value: float):
        self._force = value
