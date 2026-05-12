# HVAC System Optimization & Energy Simulation Tool

**Python-based framework** for modeling annual HVAC energy consumption, operating costs, and CO₂ emissions for a commercial building in Ottawa, Canada.

This project demonstrates practical **systems engineering**, **climate-responsive simulation**, and **data-driven optimization** skills — ideal for Mechanical, Energy, Building Systems, or Simulation Engineering roles.

![Hourly Energy Consumption](results/hourly_energy.png)
![Savings Comparison](results/savings_comparison.png)

## Key Features
- Realistic Ottawa climate load profile (monthly temperature interpolation + daily business-hour variation)
- Modular HVAC component modeling with part-load efficiency curves
- 6 practical upgrade scenarios
- Sensitivity analysis, Monte Carlo uncertainty (5,000 runs), and SciPy parametric optimization
- Automated professional PDF report generation

## Technologies
- Python 3
- NumPy, Pandas, Matplotlib, SciPy
- Object-oriented modular design

## Results Summary (Latest Run)

| Scenario                    | Annual Energy (kWh) | Cost Savings ($) | Energy Savings (kWh) | Savings % | ROI (years) | CO₂ Reduction (tons) |
|-----------------------------|---------------------|------------------|----------------------|-----------|-------------|----------------------|
| **Baseline**                | 662,256             | -                | -                    | -         | -           | -                    |
| VFD Fans & Pumps            | 646,488             | 1,892            | 15,768               | 2.4%      | 26.4        | 7.9                  |
| Thermostat Optimization     | 623,362             | 4,667            | 38,894               | 5.9%      | 10.7        | 19.4                 |
| **High Efficiency Chiller** | **609,696**         | **6,307**        | **52,560**           | **7.9%**  | **7.9**     | **26.3**             |
| LED Lighting Retrofit       | 623,362             | 4,415            | 38,894               | 5.9%      | 11.3        | 18.4                 |
| Economizer + DCV            | 625,990             | 4,351            | 36,266               | 5.5%      | 11.5        | 18.1                 |
| **Combined Measures**       | **537,163**         | **15,011**       | **125,093**          | **18.9%** | **3.3**     | **62.5**             |

**Best performer**: Combined Measures delivers strong ~19% energy reduction with excellent ROI.

## Advanced Analysis
- **Sensitivity Analysis**: Strong correlation between electricity price, investment cost, and overall savings
- **Monte Carlo (5,000 runs)**: Mean ROI 3.5 years with very high probability of positive outcomes
- **Parametric Optimization**: SciPy identified further improvements beyond manual scenarios

## Getting Started

```bash
git clone https://github.com/ZMatrix253/HVAC_Optimization_Project.git
cd HVAC_Optimization_Project

python3 -m venv venv
source venv/bin/activate        # macOS / Linux

pip install numpy pandas matplotlib scipy

python main.py