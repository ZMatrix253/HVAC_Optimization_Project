# main.py
import numpy as np
import pandas as pd
from hvac_components import HVACComponent
from simulation import simulate_hvac, generate_hourly_load
from optimization import apply_scenario, calculate_roi
from visualization import plot_hourly_energy, plot_savings

# -----------------------------
# Generate hourly load profile
# -----------------------------
hourly_load = generate_hourly_load()

# -----------------------------
# Define baseline HVAC components
# -----------------------------
components = [
    HVACComponent("Chiller", 30),
    HVACComponent("Boiler", 15),
    HVACComponent("Fans", 5),
    HVACComponent("Pumps", 5)
]

# -----------------------------
# Baseline simulation
# -----------------------------
baseline_energy, baseline_co2 = simulate_hvac(components, hourly_load)
baseline_cost = np.sum(baseline_energy) * 0.12  # $/kWh

print(f"Baseline annual energy: {np.sum(baseline_energy):,.0f} kWh")
print(f"Baseline annual cost: ${baseline_cost:,.2f}")

# -----------------------------
# Optimization scenarios
# -----------------------------
scenarios = {
    "VFD Fans & Pumps": {"Fans": 4, "Pumps": 4},
    "Thermostat Optimization": {"Chiller": 27, "Boiler": 13},
    "High Efficiency Chiller": {"Chiller": 24},
    "Combined Measures": {"Chiller": 24, "Boiler": 13, "Fans": 4, "Pumps": 4}
}

results = []
hourly_scenarios = []

for name, scenario in scenarios.items():
    optimized_components = apply_scenario(components, scenario)
    energy, co2 = simulate_hvac(optimized_components, hourly_load)
    cost = np.sum(energy) * 0.12
    savings_energy = np.sum(baseline_energy) - np.sum(energy)
    savings_cost = baseline_cost - cost
    roi_years = calculate_roi(50000, savings_cost)  # example cost
    results.append({
        "Scenario": name,
        "Annual Energy (kWh)": np.sum(energy),
        "Annual Cost ($)": cost,
        "Savings Energy (kWh)": savings_energy,
        "Savings Cost ($)": savings_cost,
        "ROI (years)": roi_years,
        "CO2 Reduction (tons)": np.sum(baseline_co2) - np.sum(co2)
    })
    hourly_scenarios.append(energy)

df_results = pd.DataFrame(results)
print(df_results)

# -----------------------------
# Visualizations
# -----------------------------
plot_hourly_energy(baseline_energy, hourly_scenarios, list(scenarios.keys()))
plot_savings(df_results)