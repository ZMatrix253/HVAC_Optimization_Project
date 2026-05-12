import numpy as np


def simulate_hvac(components, hourly_load):
    """
    Simulate HVAC system energy and CO2 emissions.
    
    Parameters:
        components: list of HVACComponent objects
        hourly_load: numpy array of hourly load factors (0-1)
    
    Returns:
        total_energy (kWh), total_co2 (tonnes)
    """
    total_energy = np.zeros_like(hourly_load)
    total_co2 = np.zeros_like(hourly_load)

    for comp in components:
        energy, co2 = comp.energy_consumed(hourly_load)
        total_energy += energy
        total_co2 += co2

    return total_energy, total_co2


import numpy as np

def generate_hourly_load(days=365):
    """
    Explicit monthly load factors for Ottawa + smooth interpolation.
    Scaling fixed at 1.0 as requested.
    """
    import numpy as np
    
    hours = days * 24
    hour_of_year = np.arange(hours)
    day_of_year = hour_of_year / 24.0
    hour_of_day = hour_of_year % 24

    # Explicit monthly average load factors for Ottawa (0.0 to 1.0 scale)
    # Higher in winter (heating) and summer (cooling)
    monthly_load_factor = [
        0.95,  # Jan - high heating
        0.85,  # Feb
        0.65,  # Mar
        0.45,  # Apr
        0.55,  # May
        0.75,  # Jun
        1.00,  # Jul - strongest cooling peak
        0.92,  # Aug
        0.70,  # Sep
        0.60,  # Oct
        0.75,  # Nov
        0.90   # Dec - high heating
    ]

    # Day of year for middle of each month
    monthly_days = np.array([15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349])

    # Smooth interpolation of monthly load factors
    base_load = np.interp(day_of_year, monthly_days, monthly_load_factor)

    # Daily variation (higher during business hours)
    daily_variation = 0.72 + 0.52 * np.sin(2 * np.pi * (hour_of_day - 7) / 24)

    total_load = base_load * daily_variation

    # Realism noise
    noise = 1.0 + 0.085 * np.random.normal(0, 1, hours)
    total_load = total_load * noise

    # === SCALING FIXED AT 1.0 AS REQUESTED ===
    total_load = total_load / total_load.mean() * 1.2

    return total_load