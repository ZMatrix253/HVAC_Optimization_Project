# HVAC System Optimization & Energy Simulation Tool

**Advanced Python framework** for modeling annual HVAC energy consumption, costs, and CO₂ emissions in a commercial building. Performs scenario analysis, sensitivity studies, Monte Carlo uncertainty quantification, and parametric optimization.

This project showcases strong simulation, data analysis, and engineering decision-making skills — highly relevant for mechanical, energy, and systems engineering roles.

![Hourly Energy Consumption](results/hourly_energy.png)
![Savings Comparison](results/savings_comparison.png)

## Key Features
- Realistic Ottawa climate load profile (temperature-dependent heating & cooling)
- Modular HVAC component modeling with part-load efficiency curves
- 6 realistic upgrade scenarios (including LED retrofit, Economizer + DCV)
- Sensitivity Analysis (electricity price, investment cost, climate)
- Monte Carlo simulation (5000 runs) for uncertainty quantification
- Parametric optimization using SciPy
- Automated professional PDF report generation

## Technologies
- Python 3, NumPy, Pandas, Matplotlib, SciPy
- Object-oriented design + modular architecture

## Results Summary (Latest Run)

| Scenario                    | Annual Energy (kWh) | Annual Cost ($) | Savings (kWh) | Savings ($) | ROI (years) | CO₂ Reduction (tons) |
|-----------------------------|---------------------|-----------------|---------------|-------------|-------------|----------------------|
| **Baseline**                | 358,722             | 43,047          | -             | -           | -           | -                    |
| VFD Fans & Pumps            | 347,334             | 41,680          | 11,388        | 1,367       | 36.6        | 5.7                  |
| **Combined Measures**       | **273,312**         | **32,797**      | **85,410**    | **10,249**  | **4.9**     | **42.7**             |

**Best performer**: Combined Measures delivers ~23.8% energy reduction with strong ROI.

## Advanced Analysis
- **Sensitivity Analysis**: Savings highly sensitive to electricity price and investment cost
- **Monte Carlo (5000 runs)**: Mean ROI 5.2 years | 94.3% probability ROI < 8 years
- **Parametric Optimization**: SciPy found optimal configuration saving extra ~$9,840/year vs manual Combined Measures

## Getting Started

```bash
git clone https://github.com/ZMatrix253/HVAC_Optimization_Project.git
cd HVAC_Optimization_Project

python3 -m venv venv
source venv/bin/activate        # macOS
pip install numpy pandas matplotlib scipy

python main.py
