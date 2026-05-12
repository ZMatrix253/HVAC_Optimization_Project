import matplotlib.pyplot as plt
import pandas as pd
import os

# Create results folder if it doesn't exist
os.makedirs('results', exist_ok=True)

def plot_hourly_energy(hourly_baseline, hourly_scenarios, scenario_names):
    plt.figure(figsize=(12, 6))
    plt.plot(hourly_baseline, label="Baseline", alpha=0.7, linewidth=2)
    for hourly, name in zip(hourly_scenarios, scenario_names):
        plt.plot(hourly, label=name, alpha=0.7)
    
    plt.title("Hourly HVAC Energy Consumption (kW)")
    plt.xlabel("Hour of Year")
    plt.ylabel("Power (kW)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig("results/hourly_energy.png", dpi=200, bbox_inches='tight')
    plt.show()


def plot_savings(df_results):
    plt.figure(figsize=(10, 6))
    df_results.plot(x='Scenario', y=['Savings Energy (kWh)', 'Savings Cost ($)'], kind='bar')
    plt.title("Energy & Cost Savings per Scenario")
    plt.ylabel("Savings")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig("results/savings_comparison.png", dpi=200, bbox_inches='tight')
    plt.show()