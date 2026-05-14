# src/analysis.py
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from src.optimization import apply_scenario, calculate_roi


def run_sensitivity_analysis(base_combined_savings, investment_cost, electricity_cost):
    """Run sensitivity analysis on price, investment, and climate."""
    print("\n" + "="*60)
    print("PERFORMING SENSITIVITY ANALYSIS")
    print("="*60)

    price_range = [0.08, 0.10, 0.12, 0.14, 0.16]
    investment_range = [30000, 40000, 50000, 60000, 80000]

    print("\nSensitivity to Electricity Price (Combined Measures):")
    print(f"{'Price ($/kWh)':<15} {'Annual Savings ($)':<20} {'ROI (years)':<12}")
    for price in price_range:
        new_savings = base_combined_savings * (price / electricity_cost)
        new_roi = investment_cost / new_savings if new_savings > 0 else float('inf')
        print(f"{price:<15.2f} {new_savings:<20,.0f} {new_roi:<12.1f}")

    print("\nSensitivity to Investment Cost (Combined Measures):")
    print(f"{'Investment ($)':<18} {'Annual Savings ($)':<20} {'ROI (years)':<12}")
    for inv in investment_range:
        new_roi = inv / base_combined_savings if base_combined_savings > 0 else float('inf')
        print(f"{inv:<18,.0f} {base_combined_savings:<20,.0f} {new_roi:<12.1f}")

    print("\nClimate Sensitivity (Combined Measures):")
    for increase in [0, 10, 20, 30]:
        climate_multiplier = 1 + increase / 100.0
        climate_savings = base_combined_savings * climate_multiplier
        climate_roi = investment_cost / climate_savings if climate_savings > 0 else float('inf')
        print(f"+{increase}% cooling demand → Savings: ${climate_savings:,.0f} | ROI: {climate_roi:.1f} years")


def run_monte_carlo(base_annual_savings, n_simulations=5000):
    """Run Monte Carlo simulation for ROI uncertainty."""
    print("\n" + "="*70)
    print("MONTE CARLO SIMULATION - Uncertainty in Savings & ROI")
    print("="*70)

    np.random.seed(42)

    electricity_price = np.random.normal(0.12, 0.025, n_simulations)
    investment_cost = np.random.normal(50000, 8000, n_simulations)
    cooling_demand_multiplier = np.random.normal(1.0, 0.12, n_simulations)

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

    prob_roi_under_8 = (df_mc['ROI (years)'] <= 8).mean() * 100
    prob_roi_under_10 = (df_mc['ROI (years)'] <= 10).mean() * 100

    print(f"\nProbability ROI < 8 years : {prob_roi_under_8:.1f}%")
    print(f"Probability ROI < 10 years: {prob_roi_under_10:.1f}%")
    print(f"Mean ROI               : {df_mc['ROI (years)'].mean():.1f} years")
    print(f"95% Confidence Interval for ROI: "
          f"{np.percentile(df_mc['ROI (years)'], 2.5):.1f} - "
          f"{np.percentile(df_mc['ROI (years)'], 97.5):.1f} years")

    return df_mc


def run_parametric_optimization(baseline_components, hourly_load, electricity_cost):
    """Run SciPy parametric optimization to find best component ratings."""
    print("\n" + "="*70)
    print("PARAMETRIC OPTIMIZATION - Finding Best Upgrade Combination")
    print("="*70)

    # Order: Chiller, Boiler, Fans, Pumps, Lighting
    initial_guess = [0.90, 0.92, 0.85, 0.88, 0.50]

    bounds = [
        (0.75, 1.0), (0.80, 1.0), (0.65, 1.0), (0.70, 1.0), (0.40, 1.0)
    ]

    def objective(x):
        scenario = {
            "Chiller": 30 * x[0],
            "Boiler": 15 * x[1],
            "Fans": 5 * x[2],
            "Pumps": 5 * x[3],
            "Lighting": 8 * x[4]
        }
        optimized_components = apply_scenario(baseline_components, scenario)
        energy, _ = simulate_hvac(optimized_components, hourly_load)  # simulate_hvac needs to be imported
        return np.sum(energy) * electricity_cost

    from src.simulation import simulate_hvac   # local import to avoid circular issues

    result = minimize(objective, initial_guess, bounds=bounds, method='L-BFGS-B')

    print(f"Optimization successful: {result.success}")
    print(f"Minimum annual cost found: ${result.fun:,.2f}")

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
        orig = next((c.nominal_power_kw for c in baseline_components if c.name == component), 0)
        reduction = (1 - optimal_reductions[list(optimal_powers.keys()).index(component)]) * 100
        print(f"  {component:12}: {power:5.1f} kW  ({reduction:4.1f}% reduction)")

    return result, optimal_powers