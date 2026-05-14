import unittest
import numpy as np

from src.hvac_components import HVACComponent
from src.simulation import simulate_hvac


class TestHVACModel(unittest.TestCase):

    def test_component_creation(self):
        """Test basic component creation."""
        chiller = HVACComponent("Chiller", 30)
        self.assertEqual(chiller.name, "Chiller")
        self.assertEqual(chiller.nominal_power_kw, 30)

    def test_energy_is_positive(self):
        """Energy output should never be negative."""
        comp = HVACComponent("Chiller", 30)
        load = np.array([0.0, 0.5, 1.0, 1.5])
        energy, _ = comp.energy_consumed(load)
        self.assertTrue(np.all(energy >= 0))

    def test_simulation_runs(self):
        """Full simulation should run and return correct shape."""
        hourly_load = np.ones(8760) * 0.8
        components = [
            HVACComponent("Chiller", 30),
            HVACComponent("Boiler", 15),
        ]
        energy, co2 = simulate_hvac(components, hourly_load)
        
        self.assertEqual(len(energy), 8760)
        self.assertTrue(np.sum(energy) > 0)


if __name__ == '__main__':
    unittest.main()