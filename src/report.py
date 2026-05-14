# src/report.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def generate_pdf_report(config, df_results, baseline_energy, hourly_scenarios,
                       baseline_components, optimal_powers, result, df_mc,
                       baseline_cost):
    """Generate the full professional PDF report."""
    print("\nGenerating professional PDF report...")

    report_filename = "results/HVAC_Optimization_Report.pdf"

    with PdfPages(report_filename) as pdf:
        # Title Page
        fig = plt.figure(figsize=(11, 8.5))
        plt.axis('off')
        plt.text(0.5, 0.92, "HVAC System Optimization Report", fontsize=24, ha='center', fontweight='bold')
        plt.text(0.5, 0.82, "Ottawa Commercial Building Case Study", fontsize=16, ha='center')
        plt.text(0.5, 0.72, "Generated: April 12, 2026", fontsize=12, ha='center')
        plt.text(0.5, 0.45, "Zoltan Marton\nHVAC Optimization Project", fontsize=13, ha='center', style='italic')
        plt.text(0.5, 0.35, "Realistic TMYx Weather • Part-Load Curves • Monte Carlo Analysis", fontsize=11, ha='center')
        pdf.savefig(fig, dpi=300)
        plt.close()

        # Executive Summary
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
"""

        plt.text(0.1, 0.88, summary_text, fontsize=11.5, va='top', fontfamily='monospace', linespacing=1.6)
        pdf.savefig(fig, dpi=300)
        plt.close()

        # Hourly Energy Plot
        plt.figure(figsize=(12, 6))
        plt.plot(baseline_energy, label="Baseline", alpha=0.85, linewidth=2.5)
        for hourly, name in zip(hourly_scenarios, config["scenarios"].keys()):
            plt.plot(hourly, label=name, alpha=0.75, linewidth=1.8)

        plt.title("Hourly HVAC Energy Consumption Over One Year", fontsize=14, fontweight='bold')
        plt.xlabel("Hour of Year", fontsize=12)
        plt.ylabel("Power (kW)", fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        pdf.savefig(plt.gcf(), dpi=300)
        plt.close()

        # Savings Comparison
        plt.figure(figsize=(11, 6))
        ax = df_results.plot(x='Scenario', y=['Savings Energy (kWh)', 'Savings Cost ($)'],
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

        # Part-Load Curves
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        axes = axes.flatten()
        for i, comp in enumerate(baseline_components):
            comp.plot_part_load_curve(ax=axes[i])
        for j in range(len(baseline_components), len(axes)):
            axes[j].axis('off')
        plt.tight_layout()
        pdf.savefig(fig, dpi=300)
        plt.close()

        # Monte Carlo Distribution
        fig = plt.figure(figsize=(10, 6))
        plt.hist(df_mc['ROI (years)'], bins=30, alpha=0.85, color='steelblue', edgecolor='black')
        plt.title("Monte Carlo Simulation — ROI Distribution (5,000 runs)", fontsize=14, fontweight='bold')
        plt.xlabel("ROI (years)")
        plt.ylabel("Frequency")
        plt.grid(True, alpha=0.3)
        pdf.savefig(fig, dpi=300)
        plt.close()

        # Optimal Configuration
        fig = plt.figure(figsize=(11, 7))
        plt.axis('off')
        plt.text(0.1, 0.95, "Optimal Configuration from Parametric Optimization", fontsize=16, fontweight='bold')

        opt_text = "Recommended Upgraded Component Ratings:\n\n"
        for component, power in optimal_powers.items():
            orig = next((c.nominal_power_kw for c in baseline_components if c.name == component), 0)
            reduction_pct = (1 - power/orig) * 100 if orig > 0 else 0
            opt_text += f"    {component:12} : {power:5.1f} kW   ({reduction_pct:5.1f}% reduction)\n"

        plt.text(0.1, 0.82, opt_text, fontsize=13, va='top', fontfamily='monospace')
        pdf.savefig(fig, dpi=300)
        plt.close()

    print(f"PDF Report successfully generated: {report_filename}")