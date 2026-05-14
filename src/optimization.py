from src.hvac_components import HVACComponent


def apply_scenario(components, scenario):
    """Update component power ratings based on the selected scenario."""
    updated = []
    for comp in components:
        # Get new power if specified in scenario, otherwise keep original
        new_power = scenario.get(comp.name, comp.nominal_power_kw)
        updated.append(HVACComponent(comp.name, new_power, comp.co2_factor))
    
    return updated


def calculate_roi(investment_cost: float, annual_savings: float) -> float:
    """Simple payback period in years."""
    if annual_savings <= 0:
        return float('inf')
    return investment_cost / annual_savings