class Dof:
    id_counter = 1

    def __init__(self):
        self.id = Dof.id_counter
        self._restrained = False
        Dof.id_counter += 1

    @property
    def restrained(self):
        return self._restrained

    @restrained.setter
    def restrained(self, value: bool):
        self.restrained = value
