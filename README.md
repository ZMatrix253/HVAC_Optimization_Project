# HVAC System Optimization & Energy Simulation Tool

**Python simulation framework** that models annual HVAC energy consumption, cost, and CO₂ emissions for a commercial building and evaluates multiple efficiency upgrade scenarios.

Demonstrates practical engineering optimization: comparing baseline HVAC performance against VFDs, thermostat tuning, high-efficiency equipment, and combined measures.

![Hourly Energy Plot](results/hourly_energy.png)

## Features
- Realistic hourly load profile generation (daily + seasonal variation)
- Modular HVAC component modeling
- Baseline vs. scenario comparison
- Energy, cost, and CO₂ savings calculation
- Simple ROI (payback period) analysis
- Automated Matplotlib visualizations

## Technologies
- Python 3
- NumPy, Pandas, Matplotlib
- Object-oriented design

## Key Results (Example Run)
| Scenario                  | Annual Energy (kWh) | Savings (kWh) | Savings ($) | ROI (years) |
|---------------------------|---------------------|---------------|-------------|-------------|
| Baseline                  | ~1,314,000         | -             | -           | -           |
| VFD Fans & Pumps          | ...                | Moderate      | ...         | ...         |
| Combined Measures         | Lowest             | Highest       | Best        | ~4–6 years  |

*(Actual numbers appear when you run `main.py`)*

## Getting Started

### 1. Clone & Install
```bash
git clone https://github.com/ZMatrix253/HVAC_Optimization_Project.git
cd HVAC_Optimization_Project
pip install numpy pandas matplotlib
