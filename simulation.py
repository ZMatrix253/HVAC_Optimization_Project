import numpy as np

def simulate_hvac(components, hourly_load):
    """
    Simulate HVAC system energy and CO2 emissions.
    
    components: list of HVACComponent objects
    hourly_load: numpy array of hourly load factors (0-1)
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
    Generates separate heating and cooling loads for Ottawa, Canada.
    Returns total_load for compatibility with current main.py
    """
    import numpy as np
    
    hours = days * 24
    hour_of_year = np.arange(hours)
    hour_of_day = hour_of_year % 24
    day_of_year = hour_of_year / 24.0

    # Daily variation (higher during business hours)
    daily_variation = 0.75 + 0.45 * np.sin(2 * np.pi * (hour_of_day - 8) / 24)

    # Realistic Ottawa temperature profile
    base_temp = 8.5 + 13.0 * np.sin(2 * np.pi * (day_of_year - 196) / 365)
    temp = base_temp + 6.0 * np.sin(2 * np.pi * hour_of_day / 24)

    # ================== SEPARATE LOADS ==================
    # Cooling load (dominant in summer)
    cooling_load = np.maximum(0.0, (temp - 18.0) * 0.055)
    
    # Heating load (dominant in winter)
    heating_load = np.maximum(0.0, (15.0 - temp) * 0.048)

    # Total HVAC load factor (for current main.py compatibility)
    total_load = daily_variation * (cooling_load * 1.25 + heating_load * 1.05 + 0.35)

    # Add realism noise
    noise = 1.0 + 0.07 * np.random.normal(0, 1, hours)
    total_load = total_load * noise

    # Normalize to reasonable average
    total_load = np.clip(total_load / total_load.mean() * 0.68, 0.1, 1.3)

    return total_load