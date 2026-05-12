import numpy as np
import pandas as pd
from hvac_components import HVACComponent
from simulation import simulate_hvac, generate_hourly_load
from optimization import apply_scenario, calculate_roi
from visualization import plot_hourly_energy, plot_savings

# ================== CONSTANTS & ASSUMPTIONS ==================
ELECTRICITY_COST = 0.12      # $/kWh (Ottawa commercial rate)
INVESTMENT_COST = 50000.0    # $ assumed capital cost for ROI calculations
CO2_GRID_FACTOR = 0.0005     # tonnes CO2 per kWh (Ontario grid average)

print("Starting HVAC System Optimization Simulation...\n")

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
    HVACComponent("Pumps", 5),
    HVACComponent("Lighting", 8)          # Added for LED retrofit scenario
]

# -----------------------------
# Baseline simulation
# -----------------------------
baseline_energy, baseline_co2 = simulate_hvac(components, hourly_load)
baseline_cost = np.sum(baseline_energy) * ELECTRICITY_COST

print(f"Baseline annual energy: {np.sum(baseline_energy):,.0f} kWh")
print(f"Baseline annual cost: ${baseline_cost:,.2f}\n")

# -----------------------------
# Realistic Optimization Scenarios
# -----------------------------
scenarios = {
    "VFD Fans & Pumps":                 {"Fans": 4, "Pumps": 4},
    "Thermostat Optimization":          {"Chiller": 27, "Boiler": 13},
    "High Efficiency Chiller":          {"Chiller": 24},
    "LED Lighting Retrofit":            {"Lighting": 3},                    # ~60% reduction
    "Economizer + DCV":                 {"Fans": 4.2, "Chiller": 27},       # Free cooling + reduced fan power
    "Combined Measures":                {"Chiller": 24, "Boiler": 13, 
                                         "Fans": 4, "Pumps": 4, "Lighting": 3}
}

results = []
hourly_scenarios = []

print("Running scenarios...\n")

for name, scenario in scenarios.items():
    optimized_components = apply_scenario(components, scenario)
    energy, co2 = simulate_hvac(optimized_components, hourly_load)
    cost = np.sum(energy) * ELECTRICITY_COST
    savings_energy = np.sum(baseline_energy) - np.sum(energy)
    savings_cost = baseline_cost - cost
    roi_years = calculate_roi(INVESTMENT_COST, savings_cost)
    
    results.append({
        "Scenario": name,
        "Annual Energy (kWh)": round(np.sum(energy)),
        "Annual Cost ($)": round(cost, 2),
        "Savings Energy (kWh)": round(savings_energy),
        "Savings Cost ($)": round(savings_cost, 2),
        "ROI (years)": round(roi_years, 1),
        "CO2 Reduction (tons)": round(np.sum(baseline_co2) - np.sum(co2), 1)
    })
    hourly_scenarios.append(energy)

df_results = pd.DataFrame(results)
print(df_results)

# -----------------------------
# Visualizations
# -----------------------------
plot_hourly_energy(baseline_energy, hourly_scenarios, list(scenarios.keys()))
plot_savings(df_results)

print("\n✅ Simulation completed successfully!")
print("   Plots saved in 'results/' folder.")


# ===================================================================
# SENSITIVITY ANALYSIS
# ===================================================================
print("\n" + "="*60)
print("PERFORMING SENSITIVITY ANALYSIS")
print("="*60)

# Base values
base_electricity_price = 0.12   # $/kWh
base_investment = 50000.0       # $
base_combined_savings = savings_cost  # from the Combined Measures scenario

# Sensitivity ranges
price_range = [0.08, 0.10, 0.12, 0.14, 0.16]          # $/kWh
investment_range = [30000, 40000, 50000, 60000, 80000] # $

print("\nSensitivity to Electricity Price (Combined Measures):")
print(f"{'Price ($/kWh)':<15} {'Annual Savings ($)':<20} {'ROI (years)':<12}")
for price in price_range:
    new_savings = base_combined_savings * (price / base_electricity_price)
    new_roi = INVESTMENT_COST / new_savings if new_savings > 0 else float('inf')
    print(f"{price:<15.2f} {new_savings:<20,.0f} {new_roi:<12.1f}")

print("\nSensitivity to Investment Cost (Combined Measures):")
print(f"{'Investment ($)':<18} {'Annual Savings ($)':<20} {'ROI (years)':<12}")
for inv in investment_range:
    new_roi = inv / base_combined_savings if base_combined_savings > 0 else float('inf')
    print(f"{inv:<18,.0f} {base_combined_savings:<20,.0f} {new_roi:<12.1f}")

# Optional: Climate sensitivity (increase cooling demand by X%)
print("\nClimate Sensitivity (Combined Measures):")
for increase in [0, 10, 20, 30]:
    climate_multiplier = 1 + increase / 100.0
    climate_savings = base_combined_savings * climate_multiplier
    climate_roi = INVESTMENT_COST / climate_savings if climate_savings > 0 else float('inf')
    print(f"+{increase}% cooling demand → Savings: ${climate_savings:,.0f} | ROI: {climate_roi:.1f} years")

    # ===================================================================
# MONTE CARLO SIMULATION - Uncertainty Analysis
# ===================================================================
print("\n" + "="*70)
print("MONTE CARLO SIMULATION - Uncertainty in Savings & ROI")
print("="*70)

import numpy as np

n_simulations = 5000
np.random.seed(42)  # For reproducibility

# Base values from Combined Measures scenario
base_annual_savings = savings_cost          # From earlier calculation
base_investment = INVESTMENT_COST

# Distributions for uncertain parameters
electricity_price = np.random.normal(0.12, 0.025, n_simulations)   # ±0.025 $/kWh
investment_cost = np.random.normal(50000, 8000, n_simulations)     # ±$8,000
cooling_demand_multiplier = np.random.normal(1.0, 0.12, n_simulations)  # ±12% variation

monte_carlo_results = []

for i in range(n_simulations):
    adjusted_savings = base_annual_savings * electricity_price[i] / 0.12 * cooling_demand_multiplier[i]
    roi = investment_cost[i] / adjusted_savings if adjusted_savings > 0 else float('inf')
    
    monte_carlo_results.append({
        "Simulation": i+1,
        "Electricity Price": round(electricity_price[i], 3),
        "Investment Cost": round(investment_cost[i]),
        "Annual Savings": round(adjusted_savings),
        "ROI (years)": round(roi, 2)
    })

df_mc = pd.DataFrame(monte_carlo_results)

print(f"Monte Carlo Results ({n_simulations} simulations):")
print(df_mc.describe().round(2)[['Annual Savings', 'ROI (years)']])

# Probability of good outcomes
prob_roi_under_8 = (df_mc['ROI (years)'] <= 8).mean() * 100
prob_roi_under_10 = (df_mc['ROI (years)'] <= 10).mean() * 100

print(f"\nProbability ROI < 8 years : {prob_roi_under_8:.1f}%")
print(f"Probability ROI < 10 years: {prob_roi_under_10:.1f}%")
print(f"Mean ROI               : {df_mc['ROI (years)'].mean():.1f} years")
print(f"95% Confidence Interval for ROI: "
      f"{np.percentile(df_mc['ROI (years)'], 2.5):.1f} - "
      f"{np.percentile(df_mc['ROI (years)'], 97.5):.1f} years")

# ===================================================================
# PARAMETRIC OPTIMIZATION USING SCIPY
# ===================================================================
print("\n" + "="*70)
print("PARAMETRIC OPTIMIZATION - Finding Best Upgrade Combination")
print("="*70)

from scipy.optimize import minimize

# Define variables to optimize (reduction factors for each component)
# Order: [Chiller, Boiler, Fans, Pumps, Lighting]
initial_guess = [0.8, 0.85, 0.8, 0.8, 0.4]   # starting reduction ratios

bounds = [(0.5, 1.0), (0.6, 1.0), (0.5, 1.0), (0.5, 1.0), (0.2, 1.0)]  # realistic limits

def objective(x):
    """Minimize total annual cost"""
    scenario = {
        "Chiller": 30 * x[0],
        "Boiler": 15 * x[1],
        "Fans": 5 * x[2],
        "Pumps": 5 * x[3],
        "Lighting": 8 * x[4]
    }
    optimized_components = apply_scenario(components, scenario)
    energy, _ = simulate_hvac(optimized_components, hourly_load)
    total_cost = np.sum(energy) * ELECTRICITY_COST
    return total_cost


# Run optimization
result = minimize(objective, initial_guess, bounds=bounds, method='L-BFGS-B')

print(f"Optimization successful: {result.success}")
print(f"Minimum annual cost found: ${result.fun:,.2f}")

# Extract optimal configuration
optimal_reductions = result.x
optimal_powers = {
    "Chiller": round(30 * optimal_reductions[0], 1),
    "Boiler": round(15 * optimal_reductions[1], 1),
    "Fans": round(5 * optimal_reductions[2], 1),
    "Pumps": round(5 * optimal_reductions[3], 1),
    "Lighting": round(8 * optimal_reductions[4], 1)
}

print("\nOptimal Configuration:")
for component, power in optimal_powers.items():
    reduction = (1 - optimal_reductions[list(optimal_powers.keys()).index(component)]) * 100
    print(f"  {component:12}: {power:5.1f} kW  ({reduction:4.1f}% reduction)")

# Compare with Combined Measures
print(f"\nCompared to 'Combined Measures' (${30_748:,.0f}), optimization saves an extra ${result.fun - 30_748:,.0f}/year")

# ===================================================================
# PDF REPORT GENERATION
# ===================================================================
print("\n" + "="*60)
print("GENERATING PROFESSIONAL PDF REPORT")
print("="*60)

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from datetime import datetime

report_filename = "results/HVAC_Optimization_Report.pdf"

with PdfPages(report_filename) as pdf:
    # Title Page
    fig = plt.figure(figsize=(11, 8))
    plt.axis('off')
    plt.text(0.5, 0.9, "HVAC System Optimization Report", fontsize=20, ha='center', fontweight='bold')
    plt.text(0.5, 0.75, "Ottawa Commercial Building Case Study", fontsize=14, ha='center')
    plt.text(0.5, 0.65, f"Generated: {datetime.now().strftime('%B %d, %Y')}", fontsize=12, ha='center')
    plt.text(0.5, 0.4, "Zoltan Marton\nSimulation & Systems Engineer", fontsize=12, ha='center')
    pdf.savefig(fig)
    plt.close()

    # Results Summary Page
    fig = plt.figure(figsize=(11, 8))
    plt.axis('off')
    plt.text(0.1, 0.95, "Key Results Summary", fontsize=16, fontweight='bold')
    
    text = f"""
Baseline Annual Energy : {np.sum(baseline_energy):,.0f} kWh
Baseline Annual Cost   : ${baseline_cost:,.2f}

Best Scenario: Combined Measures
    • Energy Savings     : {df_results.iloc[-1]['Savings Energy (kWh)']:,.0f} kWh ({df_results.iloc[-1]['Savings Energy (kWh)']/np.sum(baseline_energy)*100:.1f}%)
    • Cost Savings       : ${df_results.iloc[-1]['Savings Cost ($)']:,.2f}
    • ROI                : {df_results.iloc[-1]['ROI (years)']:.1f} years
    • CO₂ Reduction      : {df_results.iloc[-1]['CO2 Reduction (tons)']:.1f} tonnes
    """
    plt.text(0.1, 0.8, text, fontsize=11, va='top', fontfamily='monospace')
    pdf.savefig(fig)
    plt.close()

    # Add the two main plots
    plot_hourly_energy(baseline_energy, hourly_scenarios, list(scenarios.keys()))
    pdf.savefig(plt.gcf())
    plt.close()

    plot_savings(df_results)
    pdf.savefig(plt.gcf())
    plt.close()

    # Monte Carlo Summary (if you have it)
    if 'df_mc' in locals():
        fig = plt.figure(figsize=(10, 6))
        plt.hist(df_mc['ROI (years)'], bins=30, alpha=0.75, color='skyblue', edgecolor='black')
        plt.title("Monte Carlo Simulation - ROI Distribution")
        plt.xlabel("ROI (years)")
        plt.ylabel("Frequency")
        plt.grid(True, alpha=0.3)
        pdf.savefig(fig)
        plt.close()

print(f"✅ Professional PDF Report saved as: {report_filename}")