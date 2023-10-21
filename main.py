class NoAmmunitionError(Exception):
    pass

class OutOfRangeError(Exception):
    pass

class DestroyedError(Exception):
    pass

class Weapon:
    def __init__(self, name, ammunition, range):
        self.name = name
        self.ammunition = ammunition
        self.range = range

    def fire_at(self, x, y, z):
        if self.ammunition <= 0:
            raise NoAmmunitionError
        if (self.name == 'Missile antisurface' and z != 0) or \
           (self.name == 'Missile anti-air' and z <= 0) or \
           (self.name == 'Torpille' and z > 0):
            raise OutOfRangeError
        self.ammunition -= 1

class Vessel:
    def __init__(self, name, armament, max_hits):
        self.name = name
        self.coordinate = (0, 0, 0)
        self.armament = armament
        self.max_hits = max_hits
        self.destroyed = False

    def go_to(self, x, y, z):
        if self.destroyed:
            raise DestroyedError
        if (self.name == 'Cruiser' and z != 0) or \
           (self.name == 'Submarine' and z not in [-1, 0]) or \
           (self.name == 'Fregate' and z != 0) or \
           (self.name == 'Destroyer' and z != 0) or \
           (self.name == 'Aircraft' and z != 1):
            raise OutOfRangeError
        self.coordinate = (x, y, z)

    def get_coordinate(self):
        return self.coordinate

    def fire_at(self, x, y, z):
        if self.destroyed:
            raise DestroyedError
        if self.max_hits <= 0:
            self.destroyed = True
            raise DestroyedError
        distance = ((self.coordinate[0] - x) ** 2 + (self.coordinate[1] - y) ** 2 + (self.coordinate[2] - z) ** 2) ** 0.5
        if distance > self.armament.range:
            raise OutOfRangeError
        self.max_hits -= 1

class BattleField:
    def __init__(self, dimension_x, dimension_y):
        self.dimension_x = dimension_x
        self.dimension_y = dimension_y
        self.vessels = []

    def add_vessel(self, vessel):
        if sum(v.max_hits for v in self.vessels) + vessel.max_hits <= 22:
            for existing_vessel in self.vessels:
                if existing_vessel.coordinate == vessel.coordinate:
                    raise ValueError("Un vaisseau est positionné ici.")
            self.vessels.append(vessel)

    def receive_shot(self, x, y, z):
        for vessel in self.vessels:
            if vessel.coordinate == (x, y, z) and not vessel.destroyed:
                return True
        return False
