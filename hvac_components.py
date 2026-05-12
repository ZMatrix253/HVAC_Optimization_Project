import numpy as np

# ================== PHYSICAL CONSTANTS & ASSUMPTIONS ==================
ELECTRICITY_COST = 0.12          # $/kWh (Ottawa commercial rate 2025-2026)
CO2_GRID_FACTOR = 0.0005         # tonnes CO2 per kWh (Ontario grid average)
INVESTMENT_COST = 50000.0        # $ (assumed capital cost for ROI calculations)


class HVACComponent:
    """
    HVAC Component with realistic part-load efficiency and traceable units.
    All power values are in kW. Energy is in kWh.
    """
    def __init__(self, name: str, nominal_power_kw: float, co2_factor: float = CO2_GRID_FACTOR):
        self.name = name
        self.nominal_power_kw = nominal_power_kw          # kW at full load
        self.co2_factor = co2_factor                      # tonnes CO2 / kWh
        
        # Part-load efficiency curves (realistic for modern equipment)
        if "Chiller" in name:
            self.base_efficiency = 0.85                   # Peak efficiency / COP equivalent
            self.part_load_curve = lambda plr: max(0.40, 0.95 * plr**0.8 - 0.15 * (1 - plr)**2)
        elif "Boiler" in name:
            self.base_efficiency = 0.88
            self.part_load_curve = lambda plr: max(0.50, 0.92 * plr**0.75)
        elif "Lighting" in name:
            self.base_efficiency = 0.95
            self.part_load_curve = lambda plr: 0.98       # Lighting is almost constant efficiency
        else:  # Fans, Pumps
            self.base_efficiency = 0.75
            self.part_load_curve = lambda plr: max(0.45, 0.85 * plr**1.1)

    def energy_consumed(self, load_factor: np.ndarray):
        """
        Calculate energy consumed and CO2 emissions.
        load_factor: array of hourly values between 0.0 and 1.0
        Returns: (energy_kwh, co2_tonnes)
        """
        plr = np.clip(load_factor, 0.0, 1.0)
        
        efficiency = self.base_efficiency * self.part_load_curve(plr)
        power_draw_kw = (self.nominal_power_kw / efficiency) * plr
        
        energy_kwh = power_draw_kw                     # since it's hourly
        co2_tonnes = energy_kwh * self.co2_factor
        
        return energy_kwh, co2_tonnes