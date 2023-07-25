from stableX.degree_of_freedom import DegreeOfFreedom


class Node:
    id_counter = 1

    def __init__(self, x, y):
        self.id = Node.id_counter
        self._x = x
        self._y = y
        self._x_dof = DegreeOfFreedom()
        self._y_dof = DegreeOfFreedom()
        self._rz_dof = DegreeOfFreedom()
        Node.id_counter += 1

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def x_dof(self):
        return self._x_dof

    @x_dof.setter
    def x_dof(self, value):
        self._x_dof = value

    @property
    def y_dof(self):
        return self._y_dof

    @y_dof.setter
    def y_dof(self, value):
        self._y_dof = value

    @property
    def rz_dof(self):
        return self._rz_dof

    @rz_dof.setter
    def rz_dof(self, value):
        self._rz_dof = value

    @property
    def coordinates(self):
        return self.x, self.y

    @coordinates.setter
    def coordinates(self, value: tuple):
        self.x = value[0]
        self.y = value[1]
