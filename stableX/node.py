from stableX.degree_of_freedom import Dof


class Node:
    id_counter = 1

    def __init__(self, x, y):
        self.id = Node.id_counter
        self._x = x
        self._y = y
        self._x_dof = Dof()
        self._y_dof = Dof()
        self._z_dof = Dof()
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
    def z_dof(self):
        return self._z_dof

    @z_dof.setter
    def z_dof(self, value):
        self._z_dof = value
