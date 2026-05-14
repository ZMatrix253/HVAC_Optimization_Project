# main.py
import numpy as np
import pandas as pd
from pathlib import Path

from src.config import load_config
from src.weather import load_from_epw
from src.hvac_components import HVACComponent
from src.simulation import simulate_hvac
from src.optimization import apply_scenario, calculate_roi
from src.visualization import plot_hourly_energy, plot_savings

# New imports for the refactored modules
from src.analysis import run_sensitivity_analysis, run_monte_carlo, run_parametric_optimization
from src.report import generate_pdf_report


def main():
    print("Starting HVAC System Optimization Simulation...\n")

    # Load configuration
    config = load_config("config.yaml")
    const = config["constants"]

    # Load weather data and building load
    hourly_load, _ = load_from_epw(
        epw_path=config["weather"]["epw_path"],
        building_params=config["building"],
        target_year=config["weather"].get("target_year")
    )

    # Create baseline components
    baseline_components = [
        HVACComponent(name, power)
        for name, power in config["components"]["baseline"].items()
    ]

    # Run baseline simulation
    baseline_energy, baseline_co2 = simulate_hvac(baseline_components, hourly_load)
    baseline_cost = np.sum(baseline_energy) * const["electricity_cost_kwh"]

    print(f"Baseline annual energy: {np.sum(baseline_energy):,.0f} kWh")
    print(f"Baseline annual cost: ${baseline_cost:,.2f}\n")

    # Diagnostics
    print("=== Baseline Power Statistics ===")
    print(f"Min  Power : {baseline_energy.min():.2f} kW")
    print(f"Mean Power : {baseline_energy.mean():.2f} kW")
    print(f"Max  Power : {baseline_energy.max():.2f} kW")
    print(f"Load Factor Range: {hourly_load.min():.3f} — {hourly_load.max():.3f}x")

    low_hours = np.sum(baseline_energy < 20)
    print(f"Hours below 20 kW: {low_hours} ({low_hours/8760*100:.1f}%)\n")

    # Run scenarios from config
    results = []
    hourly_scenarios = []

    print("Running scenarios...\n")

    for name, scenario in config["scenarios"].items():
        optimized_components = apply_scenario(baseline_components, scenario)
        energy, co2 = simulate_hvac(optimized_components, hourly_load)
        cost = np.sum(energy) * const["electricity_cost_kwh"]

        savings_energy = np.sum(baseline_energy) - np.sum(energy)
        savings_cost = baseline_cost - cost
        roi_years = calculate_roi(const["investment_cost"], savings_cost)

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

    # Visualizations
    plot_hourly_energy(baseline_energy, hourly_scenarios, list(config["scenarios"].keys()))
    plot_savings(df_results)

    print("\nSimulation completed successfully!")
    print("Plots saved in 'results/' folder.")

    # Run advanced analysis
    base_combined_savings = savings_cost  # from last scenario (Combined Measures)

    run_sensitivity_analysis(
        base_combined_savings=base_combined_savings,
        investment_cost=const["investment_cost"],
        electricity_cost=const["electricity_cost_kwh"]
    )

    df_mc = run_monte_carlo(base_annual_savings=base_combined_savings)

    result, optimal_powers = run_parametric_optimization(
        baseline_components=baseline_components,
        hourly_load=hourly_load,
        electricity_cost=const["electricity_cost_kwh"]
    )

    # Generate PDF report
    generate_pdf_report(
        config=config,
        df_results=df_results,
        baseline_energy=baseline_energy,
        hourly_scenarios=hourly_scenarios,
        baseline_components=baseline_components,
        optimal_powers=optimal_powers,
        result=result,
        df_mc=df_mc,
        baseline_cost=baseline_cost
    )

    # Debug Sample
    print("\nSaving hourly debug sample...")
    hours_sample = list(range(0, 8760, 1000))

    debug_data = pd.DataFrame({
        'Hour': hours_sample,
        'Baseline (kW)': [baseline_energy[h] for h in hours_sample]
    })

    for i, name in enumerate(config["scenarios"].keys()):
        debug_data[name] = [hourly_scenarios[i][h] for h in hours_sample]

    print(debug_data.round(1))
    debug_data.round(1).to_csv('results/hourly_debug_sample.csv', index=False)
    print("Debug sample saved to results/hourly_debug_sample.csv")

    # Part-Load Curves Visualization
    print("\nGenerating Part-Load Efficiency Curves...")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    for i, comp in enumerate(baseline_components):
        comp.plot_part_load_curve(ax=axes[i])

    for j in range(len(baseline_components), len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.savefig("results/part_load_curves.png", dpi=300, bbox_inches='tight')
    plt.show()

    # Before vs After Part-Load Comparison
    print("\nCreating Before vs After Part-Load Comparison...")

    baseline_old = np.zeros_like(hourly_load)

    for comp in baseline_components:
        linear_comp = HVACComponent(comp.name, comp.nominal_power_kw, comp.co2_factor)
        linear_comp.part_load_curve = lambda plr: np.ones_like(plr)

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
    plt.show(block=False)
    plt.pause(2)
    plt.close()

    print("\nAll done.")


if __name__ == "__main__":
    main()