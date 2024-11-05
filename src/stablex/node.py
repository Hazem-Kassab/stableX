from stablex.degree_of_freedom import DegreeOfFreedom


class Node:
    """
     Represents a node in a 2D space with degrees of freedom.

     Parameters
     ----------
     id : int
        Unique identifier for the node.
     x : float
         The x-coordinate of the node.
     y : float
         The y-coordinate of the node.

     Attributes
     ----------
     id : int
         Unique identifier for the node.
     x : float
         The x-coordinate of the node.
     y : float
         The y-coordinate of the node.
     x_dof : DegreeOfFreedom
         Translational degree of freedom in the x-direction.
     y_dof : DegreeOfFreedom
         Translational degree of freedom in the y-direction.
     rz_dof : DegreeOfFreedom
         Rotational degree of freedom about the z-axis.

     Methods
     -------
     __str__() -> str
         Returns a string representation of the node in the format:
         "Node {id} at <x={x}, y={y}>".

     """
    id_counter = 1

    def __init__(self, x, y):
        """
        Initializes a new Node with the specified id and coordinates.

        Parameters
        ----------
        id : int
            Unique identifier for the node.
        x : float
            The x-coordinate of the node.
        y : float
            The y-coordinate of the node.

        Creates three degrees of freedom: two translational (x_dof and y_dof)
        and one rotational (rz_dof).
        """
        self.id = Node.id_counter
        self.x = x
        self.y = y
        self._x_original = x
        self._y_original = y
        self.x_dof = DegreeOfFreedom()
        self.y_dof = DegreeOfFreedom()
        self.rz_dof = DegreeOfFreedom()
        Node.id_counter += 1

    @property
    def coordinates(self) -> tuple:
        """Gets and sets the coordinates of the node as a tuple (x, y)."""
        return self.x, self.y

    @coordinates.setter
    def coordinates(self, coords: tuple):
        self.x, self.y = coords

    def __str__(self):
        """Returns a string representation of the node."""
        return f"Node {self.id} at <x={self.x}, y={self.y}>"
