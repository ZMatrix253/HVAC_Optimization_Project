class HVACComponent:
    def __init__(self, name, power_kw, co2_factor=0.0005):
        """
        name: component name
        power_kw: nominal power in kW
        co2_factor: tons of CO2 per kWh
        """
        self.name = name
        self.power_kw = power_kw
        self.co2_factor = co2_factor
    
    def energy_consumed(self, load_factor):
        """
        load_factor: numpy array of hourly load factor (0-1)
        Returns energy in kWh and CO2 emissions in tons
        """
        import numpy as np
        energy = self.power_kw * load_factor
        co2 = energy * self.co2_factor
        return energy, co2