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
    Generates a realistic hourly HVAC load profile for Ottawa, Canada.
    - Peak cooling in mid-July (summer)
    - Higher heating demand in winter
    """
    import numpy as np
    
    hours = days * 24
    hour_of_year = np.arange(hours)
    
    # Daily variation (higher during daytime)
    daily_variation = 0.8 + 0.4 * np.sin(2 * np.pi * (hour_of_year % 24) / 24 - np.pi/2)
    
    # Seasonal variation - More realistic for Ottawa
    # Peak cooling around day 200 (mid-July)
    day_of_year = hour_of_year / 24
    seasonal_cooling = np.sin(2 * np.pi * (day_of_year - 200) / 365)   # Peak in summer
    
    # Cooling load is stronger in summer
    cooling_factor = 0.6 + 0.8 * np.maximum(0, seasonal_cooling)
    
    # Heating load is stronger in winter (inverse of cooling)
    heating_factor = 0.6 + 0.7 * np.maximum(0, -seasonal_cooling)
    
    # Combine both (total HVAC load)
    total_load = daily_variation * (cooling_factor * 0.7 + heating_factor * 0.6)
    
    # Add some random noise for realism
    noise = 1 + 0.08 * np.random.randn(hours)
    total_load = total_load * noise
    
    # Normalize so average load factor is reasonable (~0.6-0.7)
    total_load = total_load / total_load.mean() * 0.65
    
    return total_load