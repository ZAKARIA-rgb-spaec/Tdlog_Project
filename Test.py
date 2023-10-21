import unittest
from main import Weapon
from main import Vessel
from main import BattleField
from main import OutOfRangeError
from main import NoAmmunitionError , DestroyedError

class TestWeapon(unittest.TestCase):

    def test_fire_at_valid(self):
        weapon = Weapon('Missile antisurface', ammunition=10, range=100)
        weapon.fire_at(10, 10, 0)
        self.assertEqual(weapon.ammunition, 9)

    def test_fire_at_no_ammunition(self):
        weapon = Weapon('Missile antisurface', ammunition=0, range=100)
        with self.assertRaises(NoAmmunitionError):
            weapon.fire_at(10, 10, 0)

    def test_fire_at_out_of_range(self):
        weapon = Weapon('Missile antisurface', ammunition=10, range=100)
        with self.assertRaises(OutOfRangeError):  # Assurez-vous que la classe OutOfRangeError est correctement définie dans votre module principal.
            weapon.fire_at(10, 10, 101)  # Coordonnées en dehors de la portée.

class TestVessel(unittest.TestCase):

    def test_go_to_valid(self):
        vessel = Vessel('Cruiser', Weapon('Missile antisurface', ammunition=10, range=100), max_hits=6)
        vessel.go_to(10, 10, 0)
        self.assertEqual(vessel.get_coordinate(), (10, 10, 0))

    def test_go_to_out_of_range(self):
        vessel = Vessel('Cruiser', Weapon('Missile antisurface', ammunition=10, range=100), max_hits=6)
        with self.assertRaises(OutOfRangeError):
            vessel.go_to(10, 10, 1)

    def test_fire_at_valid(self):
        vessel = Vessel('Cruiser', Weapon('Missile antisurface', ammunition=10, range=100), max_hits=6)
        vessel.fire_at(10, 10, 0)
        self.assertEqual(vessel.max_hits, 5)

    def test_fire_at_no_ammunition(self):
        vessel = Vessel('Cruiser', Weapon('Missile antisurface', ammunition=0, range=100), max_hits=6)
        with self.assertRaises(NoAmmunitionError):
            vessel.fire_at(10, 10, 0)

    def test_fire_at_out_of_range(self):
        vessel = Vessel('Cruiser', Weapon('Missile antisurface', ammunition=10, range=100), max_hits=6)
        with self.assertRaises(OutOfRangeError):
            vessel.fire_at(50, 50, 150)  # Coordonnées en dehors de la portée.

class TestBattleField(unittest.TestCase):

    def test_add_vessel_valid(self):
        field = BattleField(dimension_x=100, dimension_y=100)
        vessel = Vessel('Cruiser', Weapon('Missile antisurface', ammunition=10, range=100), max_hits=6)
        field.add_vessel(vessel)
        self.assertEqual(len(field.vessels), 1)

    def test_add_vessel_overlapping(self):
        field = BattleField(dimension_x=100, dimension_y=100)
        vessel1 = Vessel('Cruiser', Weapon('Missile antisurface', ammunition=10, range=100), max_hits=6)
        vessel2 = Vessel('Submarine', Weapon('Torpille', ammunition=10, range=40), max_hits=2)
        vessel1.go_to(10, 10, 0)
        with self.assertRaises(ValueError):
            field.add_vessel(vessel2)

    def test_receive_shot_hit(self):
        field = BattleField(dimension_x=100, dimension_y=100)
        vessel = Vessel('Cruiser', Weapon('Missile antisurface', ammunition=10, range=100), max_hits=6)
        vessel.go_to(10, 10, 0)
        field.add_vessel(vessel)
        self.assertTrue(field.receive_shot(10, 10, 0))

    def test_receive_shot_miss(self):
        field = BattleField(dimension_x=100, dimension_y=100)
        vessel = Vessel('Cruiser', Weapon('Missile antisurface', ammunition=10, range=100), max_hits=6)
        field.add_vessel(vessel)
        self.assertFalse(field.receive_shot(50, 50, 0))

if __name__ == '__main':
    unittest.main()

