class NoAmmunitionError(Exception):
    pass

class OutOfRangeError(Exception):
    pass

class DestroyedError(Exception):
    pass

def calculate_distance(coord1, coord2):
    return sum((x - y) ** 2 for x, y in zip(coord1, coord2)) ** 0.5

class Weapon:
    def __init__(self, ammunitions, range):
        self.ammunitions = ammunitions
        self.range = range


    def fire_at(self, x, y, z):
        if self.ammunitions <= 0:
            raise NoAmmunitionError("Out of ammunition")
        distance = calculate_distance((x, y, z), (0, 0, 0))
        if isinstance(self, SurfaceMissile) and z != 0:
            raise OutOfRangeError("Surface missile out of range")
        if isinstance(self, AntiAirMissile) and z <= 0:
            raise OutOfRangeError("Anti-air missile out of range")
        if isinstance(self, Torpedo) and z > 0:
            raise OutOfRangeError("Torpedo out of range")
        self.ammunitions -= 1
        return True


class SurfaceMissile(Weapon):
    def __init__(self, ammunitions):
        super().__init__(ammunitions, 100)

class AntiAirMissile(Weapon):
    def __init__(self, ammunitions):
        super().__init__(ammunitions, 20)

class Torpedo(Weapon):
    def __init__(self, ammunitions):
        super().__init__(ammunitions, 40)

class Vessel:
    def __init__(self, coordinate, max_hits, weapon):
        self.coordinate = coordinate
        self.max_hits = max_hits
        self.weapon = weapon
        self.hits = max_hits

    def go_to(self, x, y, z):
        distance = calculate_distance(self.coordinate, (x, y, z))
        if self.weapon.range < calculate_distance(self.coordinate, (x, y, z)):
            raise OutOfRangeError("Vessel cannot move that far")
        self.coordinate = (x, y, z)

    def get_coordinate(self):
        return self.coordinate

    def fire_at(self, x, y, z):
        if self.hits <= 0:
            raise DestroyedError("Vessel is destroyed")
        self.weapon.fire_at(x, y, z)
        self.hits -= 1
        return True
class Cruiser(Vessel):
    def __init__(self, coordinate):
            super().__init__(coordinate, 6, SurfaceMissile(50))



class Submarine(Vessel):
    def __init__(self, coordinate):
        super().__init__(coordinate, 2, Torpedo(24))
class Fregate(Vessel):
    def __init__(self, coordinate):
        super().__init__(coordinate, 5, SurfaceMissile(40))

class Destroyer(Vessel):
    def __init__(self, coordinate):
        super().__init__(coordinate, 4, Torpedo(20))

class Aircraft(Vessel):
    def __init__(self, coordinate):
        super().__init__(coordinate, 1, SurfaceMissile(10))
class Battlefield:
    def __init__(self, x_max, y_max, z_values):
        self.x_max = x_max
        self.y_max = y_max
        self.z_values = z_values
        self.vessels = []

    def add_vessel(self, vessel):
        if vessel.coordinate in [v.get_coordinate() for v in self.vessels]:
            raise ValueError("Another vessel is already at this location")
        if sum(v.max_hits for v in self.vessels) + vessel.max_hits > 22:
            raise ValueError("Maximum hits exceeded")
        self.vessels.append(vessel)
        return True

    def receive_hit(self, x, y, z):
        for vessel in self.vessels:
            if vessel.get_coordinate() == (x, y, z):
                return True
        return False


