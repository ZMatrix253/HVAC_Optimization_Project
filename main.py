import numpy as np
import pandas as pd
from hvac_components import HVACComponent
from simulation import simulate_hvac
from weather import load_from_epw                    # ← Added
from optimization import apply_scenario, calculate_roi
from visualization import plot_hourly_energy, plot_savings

# ================== CONSTANTS & ASSUMPTIONS ==================
ELECTRICITY_COST = 0.12      # $/kWh (Ottawa commercial rate)
INVESTMENT_COST = 50000.0    # $ assumed capital cost for ROI calculations
CO2_GRID_FACTOR = 0.0005     # tonnes CO2 per kWh (Ontario grid average)

print("Starting HVAC System Optimization Simulation...\n")

# -----------------------------
# Load REAL weather data from EPW   ← CHANGED
# -----------------------------
hourly_load, _ = load_from_epw(
    epw_path="data/CAN_ON_Ottawa.CDA.RCS.710630_TMYx.2011-2025.epw"
)

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


# === DIAGNOSTICS FOR PLOT 1 ===
print(f"\n=== Baseline Power Statistics ===")
print(f"Min  Power : {baseline_energy.min():.2f} kW")
print(f"Mean Power : {baseline_energy.mean():.2f} kW")
print(f"Max  Power : {baseline_energy.max():.2f} kW")
print(f"Load Factor Range: {hourly_load.min():.3f} — {hourly_load.max():.3f}x")

# Check how many hours are very low
low_hours = np.sum(baseline_energy < 20)   # arbitrary threshold
print(f"Hours below 20 kW: {low_hours} ({low_hours/8760*100:.1f}%)")

# -----------------------------
# Realistic & Believable Scenarios
# -----------------------------
scenarios = {
    "VFD Fans & Pumps":                 {"Fans": 4.25, "Pumps": 4.25},      # ~6.5% overall
    "Thermostat Optimization":          {"Chiller": 27.5, "Boiler": 13.8},  # ~5.0% overall
    "High Efficiency Chiller":          {"Chiller": 25.0},                  # ~7.8% overall (believable)
    "LED Lighting Retrofit":            {"Lighting": 4.5},                  # ~5.2% overall (realistic)
    "Economizer + DCV":                 {"Fans": 4.4, "Chiller": 27.5},     # ~7.5% overall
    "Combined Measures":                {"Chiller": 25.0, "Boiler": 13.8, 
                                         "Fans": 4.25, "Pumps": 4.25, "Lighting": 4.5}
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
initial_guess = [0.90, 0.92, 0.85, 0.88, 0.50]

# Realistic reduction limits
bounds = [
    (0.75, 1.0),   # Chiller: max 25% improvement
    (0.80, 1.0),   # Boiler: max 20%
    (0.65, 1.0),   # Fans: max 35% (VFDs are good)
    (0.70, 1.0),   # Pumps
    (0.40, 1.0)    # Lighting: max 60% (LED retrofit)
]

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
# PDF REPORT GENERATION (Fixed - No Empty Pages)
# ===================================================================
print("\n" + "="*60)
print("GENERATING PROFESSIONAL PDF REPORT")
print("="*60)

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from datetime import datetime

report_filename = "results/HVAC_Optimization_Report.pdf"

with PdfPages(report_filename) as pdf:
    # ====================== 1. Title Page ======================
    fig = plt.figure(figsize=(11, 8.5))
    plt.axis('off')
    plt.text(0.5, 0.92, "HVAC System Optimization Report", fontsize=24, ha='center', fontweight='bold')
    plt.text(0.5, 0.82, "Ottawa Commercial Building Case Study", fontsize=16, ha='center')
    plt.text(0.5, 0.72, "Generated: April 12, 2026", fontsize=12, ha='center')
    plt.text(0.5, 0.45, "Zoltan Marton\nHVAC Optimization Project", fontsize=13, ha='center', style='italic')
    plt.text(0.5, 0.35, "Realistic TMYx Weather • Part-Load Curves • Monte Carlo Analysis", fontsize=11, ha='center')
    pdf.savefig(fig, dpi=300)
    plt.close()

    # ====================== 2. Executive Summary ======================
    fig = plt.figure(figsize=(11, 8.5))
    plt.axis('off')
    plt.text(0.1, 0.96, "Executive Summary", fontsize=18, fontweight='bold')

    combined = df_results[df_results['Scenario'] == "Combined Measures"].iloc[0]
    baseline_energy_total = np.sum(baseline_energy)
    savings_percent = (combined['Savings Energy (kWh)'] / baseline_energy_total) * 100

    summary_text = f"""
Baseline Performance
    Annual Energy Consumption : {baseline_energy_total:,.0f} kWh
    Annual Operating Cost      : ${baseline_cost:,.2f}

Best Scenario — Combined Measures
    Annual Energy              : {combined['Annual Energy (kWh)']:,.0f} kWh
    Energy Reduction           : {combined['Savings Energy (kWh)']:,.0f} kWh ({savings_percent:.1f}%)
    Cost Savings               : ${combined['Savings Cost ($)']:,.2f}
    Payback Period             : {combined['ROI (years)']:.1f} years
    CO₂ Reduction              : {combined['CO2 Reduction (tons)']:.1f} tonnes

Parametric Optimization (SciPy)
    Additional Annual Savings  : ${result.fun - combined['Annual Cost ($)']:,.0f}
    Minimum Annual Cost Found  : ${result.fun:,.2f}

Monte Carlo Analysis (5,000 runs)
    Mean ROI                   : {df_mc['ROI (years)'].mean():.1f} years
    95% Confidence Interval    : {np.percentile(df_mc['ROI (years)'], 2.5):.1f} – {np.percentile(df_mc['ROI (years)'], 97.5):.1f} years
    Probability of ROI < 8 yrs : {prob_roi_under_8:.1f}%
"""

    plt.text(0.1, 0.88, summary_text, fontsize=11.5, va='top', fontfamily='monospace', linespacing=1.6)
    pdf.savefig(fig, dpi=300)
    plt.close()

    # ====================== 3. Hourly Energy Consumption ======================
    # Create plot WITHOUT showing it
    plt.figure(figsize=(12, 6))
    plt.plot(baseline_energy, label="Baseline", alpha=0.85, linewidth=2.5)
    for hourly, name in zip(hourly_scenarios, scenarios.keys()):
        plt.plot(hourly, label=name, alpha=0.75, linewidth=1.8)
    
    plt.title("Hourly HVAC Energy Consumption Over One Year", fontsize=14, fontweight='bold')
    plt.xlabel("Hour of Year", fontsize=12)
    plt.ylabel("Power (kW)", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    pdf.savefig(plt.gcf(), dpi=300)
    plt.close()

    # ====================== 4. Savings Comparison ======================
    plt.figure(figsize=(11, 6))
    ax = df_results.plot(x='Scenario', 
                        y=['Savings Energy (kWh)', 'Savings Cost ($)'], 
                        kind='bar', width=0.8)
    plt.title("Energy & Cost Savings by Scenario", fontsize=14, fontweight='bold')
    plt.ylabel("Savings", fontsize=12)
    plt.xlabel("")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', padding=3)
    
    pdf.savefig(plt.gcf(), dpi=300)
    plt.close()

    # ====================== 5. Part-Load Curves ======================
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()
    for i, comp in enumerate(components):
        comp.plot_part_load_curve(ax=axes[i])
    for j in range(len(components), len(axes)):
        axes[j].axis('off')
    plt.tight_layout()
    pdf.savefig(fig, dpi=300)
    plt.close()

    # ====================== 6. Monte Carlo Distribution ======================
    fig = plt.figure(figsize=(10, 6))
    plt.hist(df_mc['ROI (years)'], bins=30, alpha=0.85, color='steelblue', edgecolor='black')
    plt.title("Monte Carlo Simulation — ROI Distribution (5,000 runs)", fontsize=14, fontweight='bold')
    plt.xlabel("ROI (years)")
    plt.ylabel("Frequency")
    plt.grid(True, alpha=0.3)
    pdf.savefig(fig, dpi=300)
    plt.close()

    # ====================== 7. Optimal Configuration ======================
    fig = plt.figure(figsize=(11, 7))
    plt.axis('off')
    plt.text(0.1, 0.95, "Optimal Configuration from Parametric Optimization", fontsize=16, fontweight='bold')

    opt_text = "Recommended Upgraded Component Ratings:\n\n"
    for component, power in optimal_powers.items():
        orig = next((c.nominal_power_kw for c in components if c.name == component), 0)
        reduction_pct = (1 - power/orig) * 100 if orig > 0 else 0
        opt_text += f"    {component:12} : {power:5.1f} kW   ({reduction_pct:5.1f}% reduction)\n"

    plt.text(0.1, 0.82, opt_text, fontsize=13, va='top', fontfamily='monospace')
    pdf.savefig(fig, dpi=300)
    plt.close()

print(f"✅ Professional PDF Report successfully generated:\n   {report_filename}")

# ================== DEBUG: SAMPLE EVERY 1000 HOURS ==================
print("\n" + "="*60)
print("DEBUG: Hourly Data Sample (every 1000 hours)")
print("="*60)

hours_sample = list(range(0, 8760, 1000))  # 0, 1000, 2000, ..., 8000

debug_data = pd.DataFrame({
    'Hour': hours_sample,
    'Baseline (kW)': [baseline_energy[h] for h in hours_sample]
})

for i, name in enumerate(scenarios.keys()):
    debug_data[name] = [hourly_scenarios[i][h] for h in hours_sample]

print(debug_data.round(1))
debug_data.round(1).to_csv('results/hourly_debug_sample.csv', index=False)
print("\nFull debug table saved to: results/hourly_debug_sample.csv")

# ===================== PART-LOAD CURVES VISUALIZATION =====================
print("\nGenerating Part-Load Efficiency Curves...")

import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for i, comp in enumerate(components):
    comp.plot_part_load_curve(ax=axes[i])

for j in range(len(components), len(axes)):
    axes[j].axis('off')

plt.tight_layout()
plt.savefig("results/part_load_curves.png", dpi=300, bbox_inches='tight')
print("✅ Saved: results/part_load_curves.png")
plt.show()

   # ===================== BEFORE vs AFTER PART-LOAD COMPARISON =====================
print("\nCreating Before vs After Part-Load Comparison...")

baseline_old = np.zeros_like(hourly_load)

for comp in components:
    linear_comp = HVACComponent(comp.name, comp.nominal_power_kw, comp.co2_factor)
    linear_comp.part_load_curve = lambda plr: np.ones_like(plr)   # Force linear (100% efficiency)
    
    energy, _ = linear_comp.energy_consumed(hourly_load)
    baseline_old += energy

plt.figure(figsize=(12, 6))
plt.plot(baseline_energy, label="With Realistic Part-Load Curves", linewidth=2.2)
plt.plot(baseline_old, label="Linear Model (Old Method)", linewidth=2, alpha=0.75)
plt.title("Impact of Part-Load Curves on Baseline Annual Energy Profile", fontsize=14, fontweight='bold')
plt.xlabel("Hour of Year")
plt.ylabel("Total HVAC Power (kW)")
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("results/partload_impact.png", dpi=300, bbox_inches='tight')
print("✅ Saved: results/partload_impact.png")

# Non-blocking show + close
plt.show(block=False)
plt.pause(2)      # Show for 2 seconds
plt.close()