import unittest
import numpy as np

from src.hvac_components import HVACComponent


class TestPartLoadCurves(unittest.TestCase):

    def test_chiller_curve(self):
        chiller = HVACComponent("Chiller", 100)
        plr = np.array([0.2, 0.6, 1.0])
        eff = chiller.part_load_curve(plr)
        self.assertTrue(np.all(eff >= 0.40))   # minimum efficiency
        self.assertTrue(np.all(eff <= 1.05))

    def test_fan_curve(self):
        fan = HVACComponent("Fans", 10)
        plr = np.array([0.1, 0.8, 1.2])
        eff = fan.part_load_curve(plr)
        self.assertTrue(np.all(eff >= 0.45))


if __name__ == '__main__':
    unittest.main()