# HVAC System Optimization & Energy Simulation Tool

**Python-based simulation framework** that models annual HVAC energy consumption, cost, and CO₂ emissions for a commercial building. Evaluates the impact of common efficiency upgrades and calculates potential savings and ROI.

This project demonstrates practical mechanical engineering + simulation skills: building modular system models, generating realistic load profiles, running scenario analysis, and visualizing results.

![Hourly Energy Consumption](results/hourly_energy.png)
![Savings Comparison](results/savings_comparison.png)

## Features
- Realistic hourly HVAC load profile (daily + seasonal variation for Ottawa climate)
- Modular component-based modeling (Chiller, Boiler, Fans, Pumps)
- Baseline vs. multiple upgrade scenarios
- Energy, operating cost, and CO₂ emissions calculation
- Simple ROI (payback period) analysis
- Automated Matplotlib visualizations

## Technologies
- **Python 3**
- NumPy, Pandas, Matplotlib
- Object-oriented design

## Results (Latest Run)

| Scenario                    | Annual Energy (kWh) | Annual Cost ($) | Savings (kWh) | Savings ($) | ROI (years) | CO₂ Reduction (tons) |
|-----------------------------|---------------------|-----------------|---------------|-------------|-------------|----------------------|
| **Baseline**                | 313,170             | 37,580          | -             | -           | -           | -                    |
| VFD Fans & Pumps            | 301,782             | 36,214          | 11,388        | 1,367       | 36.6        | 5.7                  |
| Thermostat Optimization     | 284,700             | 34,164          | 28,470        | 3,416       | 14.6        | 14.2                 |
| High Efficiency Chiller     | 279,006             | 33,481          | 34,164        | 4,100       | 12.2        | 17.1                 |
| **Combined Measures**       | **256,230**         | **30,748**      | **56,940**    | **6,833**   | **7.3**     | **28.5**             |

*Assumes $50,000 investment cost for ROI calculations. Results generated from `main.py`.*

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/ZMatrix253/HVAC_Optimization_Project.git
cd HVAC_Optimization_Project
