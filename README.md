# HVAC System Optimization & Energy Simulation Tool

Python-based tool for modeling annual HVAC energy use, costs, and CO₂ emissions for a commercial building in Ottawa, Canada.

This project was built to explore realistic energy efficiency upgrades using real weather data, part-load equipment behavior, and proper engineering analysis methods. It demonstrates skills in systems modeling, data-driven optimization, and practical simulation — relevant for mechanical, energy, building systems, or simulation engineering roles.

![Hourly Energy Consumption](results/hourly_energy.png)
![Savings Comparison](results/savings_comparison.png)

## Key Features

- Real Ottawa TMYx weather data (EPW) with physics-based heating/cooling load calculation
- Modular HVAC components using realistic part-load efficiency curves
- 6 practical retrofit scenarios (VFDs, high-efficiency chiller, LED lighting, economizer, etc.)
- Sensitivity analysis, Monte Carlo uncertainty (5,000 runs), and SciPy parametric optimization
- Automated PDF report generation

## Technologies

- **Python 3** (NumPy, Pandas, Matplotlib, SciPy)
- Object-oriented design with clear separation of concerns
- Real EPW weather file handling

## Results Summary (Latest Run — May 2026)

| Scenario                    | Annual Energy (kWh) | Cost Savings ($) | Energy Savings (kWh) | Savings % | ROI (years) | CO₂ Reduction (t) |
|-----------------------------|---------------------|------------------|----------------------|-----------|-------------|-------------------|
| **Baseline**                | 636,413             | -                | -                    | -         | -           | -                 |
| VFD Fans & Pumps            | 621,329             | 1,810            | 15,084               | 2.4%      | 27.6        | 7.5               |
| Thermostat Optimization     | 599,700             | 4,406            | 36,713               | 5.8%      | 11.3        | 18.4              |
| High Efficiency Chiller     | 586,621             | 5,975            | 49,792               | 7.8%      | 8.4         | 24.9              |
| LED Lighting Retrofit       | 597,306             | 4,693            | 39,107               | 6.1%      | 10.7        | 19.6              |
| Economizer + DCV            | 605,483             | 3,712            | 30,930               | 4.9%      | 13.5        | 15.5              |
| **Combined Measures**       | **520,613**         | **13,896**       | **115,800**          | **18.2%** | **3.6**     | **57.9**          |

The **Combined Measures** scenario delivers the best balance — **18.2%** energy reduction with a **3.6-year** payback.

## Advanced Analysis

- Sensitivity analysis on electricity price, investment cost, and climate variations
- Monte Carlo simulation (5,000 runs) to quantify uncertainty in ROI
- Parametric optimization using SciPy to find the best combination of upgrades

**Best configuration found:**
- Chiller: 22.5 kW (25% reduction)
- Boiler: 12.0 kW (20% reduction)
- Fans: 3.2 kW (35% reduction)
- Pumps: 3.5 kW (30% reduction)
- Lighting: 3.2 kW (60% reduction)

## Getting Started

```bash
git clone https://github.com/ZMatrix253/HVAC_Optimization_Project.git
cd HVAC_Optimization_Project

python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# Windows: venv\Scripts\activate

pip install -r requirements.txt

python main.py