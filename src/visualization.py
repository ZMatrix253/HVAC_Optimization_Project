import matplotlib.pyplot as plt
import pandas as pd
import os

# Create results folder if it doesn't exist
os.makedirs('results', exist_ok=True)


def plot_hourly_energy(hourly_baseline, hourly_scenarios, scenario_names):
    """Plot hourly energy consumption over the year."""
    plt.figure(figsize=(12, 6))
    
    # Baseline with thicker line
    plt.plot(hourly_baseline, label="Baseline", alpha=0.85, linewidth=2.5)
    
    # Plot each scenario
    for hourly, name in zip(hourly_scenarios, scenario_names):
        plt.plot(hourly, label=name, alpha=0.75, linewidth=1.8)
    
    plt.title("Hourly HVAC Energy Consumption Over One Year", fontsize=14, fontweight='bold')
    plt.xlabel("Hour of Year", fontsize=12)
    plt.ylabel("Power (kW)", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig("results/hourly_energy.png", dpi=300, bbox_inches='tight')
    print("Saved: results/hourly_energy.png")
    
    plt.show()


def plot_savings(df_results):
    """Create bar chart comparing energy and cost savings by scenario."""
    plt.figure(figsize=(11, 6))
    
    ax = df_results.plot(x='Scenario', 
                        y=['Savings Energy (kWh)', 'Savings Cost ($)'], 
                        kind='bar',
                        figsize=(11, 6),
                        width=0.8)
    
    plt.title("Energy & Cost Savings by Scenario", fontsize=14, fontweight='bold')
    plt.ylabel("Savings", fontsize=12)
    plt.xlabel("")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', padding=3)
    
    plt.savefig("results/savings_comparison.png", dpi=300, bbox_inches='tight')
    print("Saved: results/savings_comparison.png")
    
    plt.show()