# HVAC System Optimization & Energy Simulation Tool

**Python-based framework** for modeling annual HVAC energy consumption, operating costs, and CO₂ emissions for a commercial building in Ottawa, Canada.

This project demonstrates practical **systems engineering**, **climate-responsive simulation**, **part-load efficiency modeling**, and **data-driven optimization** skills — ideal for Mechanical, Energy, Building Systems, or Simulation Engineering roles.

![Hourly Energy Consumption](results/hourly_energy.png)
![Savings Comparison](results/savings_comparison.png)

## Key Features
- Realistic Ottawa TMYx weather data (2011–2025) with physics-based load calculation
- Modular HVAC components with realistic **part-load efficiency curves**
- 6 practical upgrade scenarios
- Sensitivity analysis, Monte Carlo uncertainty (5,000 runs), and SciPy parametric optimization
- Automated professional PDF report generation

## Technologies
- Python 3
- NumPy, Pandas, Matplotlib, SciPy
- Object-oriented modular design

## Results Summary (Latest Run — May 2026)

| Scenario                    | Annual Energy (kWh) | Cost Savings ($) | Energy Savings (kWh) | Savings % | ROI (years) | CO₂ Reduction (t) |
|-----------------------------|---------------------|------------------|----------------------|-----------|-------------|-------------------|
| **Baseline**                | **636,413**         | -                | -                    | -         | -           | -                 |
| VFD Fans & Pumps            | 621,329             | 1,810            | 15,084               | 2.4%      | 27.6        | 7.5               |
| Thermostat Optimization     | 599,700             | 4,406            | 36,713               | 5.8%      | 11.3        | 18.4              |
| High Efficiency Chiller     | 586,621             | 5,975            | 49,792               | 7.8%      | 8.4         | 24.9              |
| LED Lighting Retrofit       | 597,306             | 4,693            | 39,107               | 6.1%      | 10.7        | 19.6              |
| Economizer + DCV            | 605,483             | 3,712            | 30,930               | 4.9%      | 13.5        | 15.5              |
| **Combined Measures**       | **520,613**         | **13,896**       | **115,800**          | **18.2%** | **3.6**     | **57.9**          |

**Best performer**: The **Combined Measures** scenario achieves **18.2%** annual energy reduction with a strong **3.6-year payback**.

## Advanced Analysis

- **Sensitivity Analysis**: Savings and ROI respond strongly to electricity price and capital cost variations.
- **Monte Carlo Simulation** (5,000 runs): Mean ROI **3.8 years**, with **99%** probability of ROI < 8 years.
- **Parametric Optimization** (SciPy): Identified an even better configuration with **$22,756** additional annual savings compared to the Combined Measures scenario.

**Optimal Configuration Found:**
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
# On Windows: venv\Scripts\activate

pip install numpy pandas matplotlib scipy

python main.py