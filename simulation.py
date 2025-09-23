# simulation.py
import numpy as np

def simulate_hvac(components, hourly_load):
    """
    Simulate HVAC system energy and CO2 emissions.
    
    components: list of HVACComponent objects
    hourly_load: numpy array of hourly load factors
    """
    total_energy = np.zeros_like(hourly_load)
    total_co2 = np.zeros_like(hourly_load)
    
    for comp in components:
        energy, co2 = comp.energy_consumed(hourly_load)
        total_energy += energy
        total_co2 += co2
    
    return total_energy, total_co2

def generate_hourly_load(days=365):
    """
    Generates an hourly HVAC load profile for a year.
    Combines daily sinusoidal variation + seasonal factor.
    """
    daily_variation = np.sin(np.linspace(0, 2*np.pi, 24)) * 0.3 + 1
    hourly_load = np.tile(daily_variation, days)
    # Seasonal variation (summer peak)
    seasonal_factor = 1 + 0.2 * np.sin(np.linspace(0, 2*np.pi, days))
    seasonal_factor_hourly = np.repeat(seasonal_factor, 24)
    return hourly_load * seasonal_factor_hourly