import numpy as np


def simulate_hvac(components, hourly_load):
    """Run the full yearly HVAC simulation and return total energy and CO2."""
    total_energy = np.zeros_like(hourly_load)
    total_co2 = np.zeros_like(hourly_load)

    for comp in components:
        energy, co2 = comp.energy_consumed(hourly_load)
        total_energy += energy
        total_co2 += co2

    return total_energy, total_co2


# Optional: old synthetic load generator (kept for reference / fallback)
def generate_hourly_load(days=365):
    """Generate synthetic hourly load profile - only used if no real weather data."""
    hours = days * 24
    hour_of_year = np.arange(hours)
    day_of_year = hour_of_year / 24.0
    hour_of_day = hour_of_year % 24

    # Rough monthly variation
    monthly_load_factor = [0.95, 0.85, 0.65, 0.45, 0.55, 0.75, 1.00, 0.92, 0.70, 0.60, 0.75, 0.90]
    monthly_days = np.array([15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349])
    base_load = np.interp(day_of_year, monthly_days, monthly_load_factor)

    # Daily pattern
    daily_variation = 0.72 + 0.52 * np.sin(2 * np.pi * (hour_of_day - 7) / 24)
    total_load = base_load * daily_variation

    # Add some noise
    noise = 1.0 + 0.085 * np.random.normal(0, 1, hours)
    total_load = total_load * noise
    total_load = total_load / total_load.mean() * 1.2
    
    return total_load