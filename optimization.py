from hvac_components import HVACComponent

def apply_scenario(components, scenario):
    """
    Apply optimization scenario by updating component power ratings.
    scenario: dict like {"Chiller": 24, "Fans": 4}
    """
    updated = []
    for comp in components:
        new_power = scenario.get(comp.name, comp.power_kw)
        updated.append(HVACComponent(comp.name, new_power, comp.co2_factor))
    return updated


def calculate_roi(investment_cost: float, annual_savings: float) -> float:
    """Simple payback period in years"""
    if annual_savings <= 0:
        return float('inf')
    return investment_cost / annual_savings
