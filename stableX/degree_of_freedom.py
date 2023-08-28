class DegreeOfFreedom:
    id_counter = 1

    def __init__(self):
        self.id = DegreeOfFreedom.id_counter
        self.restrained = False
        self.displacement = 0
        DegreeOfFreedom.id_counter += 1
        self.force = 0

    @property
    def restrained(self):
        return self._restrained

    @restrained.setter
    def restrained(self, value: bool):
        self._restrained = value

    @property
    def force(self):
        return self._force

    @force.setter
    def force(self, value):
        self._force = value

    @property
    def displacement(self):
        return self._displacement

    @displacement.setter
    def displacement(self, value):
        self._displacement = value
