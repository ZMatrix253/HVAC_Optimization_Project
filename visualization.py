# visualization.py
import matplotlib.pyplot as plt
import pandas as pd

def plot_hourly_energy(hourly_baseline, hourly_scenarios, scenario_names):
    plt.figure(figsize=(12,6))
    plt.plot(hourly_baseline, label="Baseline", alpha=0.7)
    for hourly, name in zip(hourly_scenarios, scenario_names):
        plt.plot(hourly, label=name, alpha=0.7)
    plt.title("Hourly HVAC Energy Consumption (kW)")
    plt.xlabel("Hour of Year")
    plt.ylabel("Power (kW)")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_savings(df_results):
    df_results.plot(x='Scenario', y=['Savings Energy (kWh)', 'Savings Cost ($)'], kind='bar', figsize=(10,6))
    plt.title("Energy & Cost Savings per Scenario")
    plt.ylabel("Savings")
    plt.tight_layout()
    plt.show()