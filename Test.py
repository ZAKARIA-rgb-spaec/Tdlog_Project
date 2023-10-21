import unittest
from main import  SurfaceMissile , AntiAirMissile, Torpedo , NoAmmunitionError ,OutOfRangeError,Battlefield,Cruiser,DestroyedError

class TestWeapon(unittest.TestCase):
    def test_surface_missile_fire_at(self):
        surface_missile = SurfaceMissile(10)
        self.assertTrue(surface_missile.fire_at(10, 10, 0))

    def test_anti_air_missile_fire_at(self):
        anti_air_missile = AntiAirMissile(10)
        self.assertTrue(anti_air_missile.fire_at(10, 10, 1))

    def test_torpedo_fire_at(self):
        torpedo = Torpedo(10)
        self.assertTrue(torpedo.fire_at(10, 10, -1))

    def test_weapon_fire_at_out_of_ammunition(self):
        surface_missile = SurfaceMissile(0)
        with self.assertRaises(NoAmmunitionError):
            surface_missile.fire_at(10, 10, 0)

    def test_weapon_fire_at_out_of_range(self):
        anti_air_missile = AntiAirMissile(10)
        with self.assertRaises(OutOfRangeError):
            anti_air_missile.fire_at(10, 10, 0)

class TestVessel(unittest.TestCase):
    def test_vessel_fire_at(self):
        vessel = Cruiser((0, 0, 0))
        self.assertTrue(vessel.fire_at(10, 10, 0))

    def test_vessel_fire_at_destroyed(self):
        vessel = Cruiser((0, 0, 0))
        vessel.hits = 0
        with self.assertRaises(DestroyedError):
            vessel.fire_at(10, 10, 0)

class TestBattlefield(unittest.TestCase):
    def test_battlefield_add_vessel(self):
        battlefield = Battlefield(100, 100, [-1, 0, 1])
        vessel = Cruiser((0, 0, 0))
        self.assertTrue(battlefield.add_vessel(vessel))

    def test_battlefield_add_vessel_same_location(self):
        battlefield = Battlefield(100, 100, [-1, 0, 1])
        vessel1 = Cruiser((0, 0, 0))
        vessel2 = Cruiser((0, 0, 0))
        with self.assertRaises(ValueError):
            battlefield.add_vessel(vessel1)
            battlefield.add_vessel(vessel2)



    def test_battlefield_receive_hit(self):
        battlefield = Battlefield(100, 100, [-1, 0, 1])
        vessel = Cruiser((0, 0, 0))
        battlefield.add_vessel(vessel)
        self.assertTrue(battlefield.receive_hit(0, 0, 0))
        self.assertFalse(battlefield.receive_hit(10, 10, 1))





if __name__ == '__main__':
    unittest.main()



