# HVAC System Optimization & Energy Simulation Tool

**Python-based building energy modeling tool** for evaluating annual HVAC energy consumption, costs, and CO₂ emissions for a commercial office building in Ottawa, Canada.

This project demonstrates a practical, engineering-driven approach to energy retrofit analysis using real weather data, realistic equipment behavior, and robust decision-support methods.

![Hourly Energy Consumption](results/hourly_energy.png)
![Savings Comparison](results/savings_comparison.png)

## Key Features

- Real Ottawa TMYx weather data (EPW) with physics-based heating, cooling, solar, and internal load calculations
- Modular HVAC components featuring **realistic part-load efficiency curves**
- Six practical retrofit scenarios (VFDs, high-efficiency chiller, LED lighting, economizer + DCV, etc.)
- Advanced analytics: sensitivity analysis, Monte Carlo uncertainty (5,000 runs), and SciPy parametric optimization
- Automated professional PDF report with executive summary and visualizations

## Results Summary (May 2026 Run)

| Scenario                    | Annual Energy (kWh) | Cost Savings ($) | Energy Savings (kWh) | Savings % | ROI (years) | CO₂ Reduction (t) |
|-----------------------------|---------------------|------------------|----------------------|-----------|-------------|-------------------|
| **Baseline**                | 636,413             | -                | -                    | -         | -           | -                 |
| VFD Fans & Pumps            | 621,329             | 1,810            | 15,084               | 2.4%      | 27.6        | 7.5               |
| Thermostat Optimization     | 599,700             | 4,406            | 36,713               | 5.8%      | 11.3        | 18.4              |
| High Efficiency Chiller     | 586,621             | 5,975            | 49,792               | 7.8%      | 8.4         | 24.9              |
| LED Lighting Retrofit       | 597,306             | 4,693            | 39,107               | 6.1%      | 10.7        | 19.6              |
| Economizer + DCV            | 605,483             | 3,712            | 30,930               | 4.9%      | 13.5        | 15.5              |
| **Combined Measures**       | **520,613**         | **13,896**       | **115,800**          | **18.2%** | **3.6**     | **57.9**          |

**Best performer**: The *Combined Measures* scenario achieves **18.2%** energy reduction with a strong **3.6-year payback**.

## Model Validation

Benchmarked against real hourly electricity meter data from the **ASHRAE Great Energy Predictor III** dataset for a comparable office building (~2,500 m²). Results were normalized by floor area and used as a high-level reasonableness check.
- **Annual energy difference**: **-0.4%**
- Strong agreement for a first-principles physics-based model.

## Technologies

- **Python 3** — NumPy, Pandas, Matplotlib, SciPy
- Object-oriented modular design with YAML configuration
- Clean separation between weather processing, component modeling, simulation, analysis, and reporting

## Advanced Analysis

- Sensitivity analysis on electricity price, investment cost, and climate variations
- Monte Carlo simulation (5,000 runs) to quantify ROI uncertainty
- Parametric optimization using SciPy to determine optimal component ratings

## Limitations & Assumptions

- Simplified single-zone 2000 m² building archetype (does not model detailed envelope dynamics, thermal mass, or multi-zone effects)
- Part-load efficiency curves are representative approximations based on ASHRAE guidelines and manufacturer data (not site-specific or fully temperature-dependent)
- Components modeled independently (no plant-level sequencing or system interactions)
- Simple payback period only (no NPV, IRR, LCC, incentives, or maintenance savings)
- Investment costs are high-level estimates (±30–50% accuracy)
- Uses TMYx typical meteorological year (does not account for climate change or extreme weather)

## Future Work

- Multi-zone capability and detailed envelope modeling
- EnergyPlus integration for validation and benchmarking
- Time-of-use tariffs and demand charge modeling
- Streamlit interactive dashboard
- Support for additional climates and building types
- Expanded validation against more ASHRAE buildings

## Getting Started

```bash
git clone https://github.com/ZMatrix253/HVAC_Optimization_Project.git
cd HVAC_Optimization_Project

python -m venv venv
source venv/bin/activate          # macOS / Linux
# On Windows: venv\Scripts\activate

pip install -r requirements.txt
python main.py