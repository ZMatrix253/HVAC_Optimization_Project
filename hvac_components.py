import numpy as np

class HVACComponent:
    """
    HVAC Component with realistic part-load performance.
    """
    def __init__(self, name: str, nominal_power_kw: float, co2_factor: float = 0.0005):
        self.name = name
        self.nominal_power_kw = nominal_power_kw
        self.co2_factor = co2_factor
        
        # Part-load efficiency curves
        if "Chiller" in name:
            self.base_efficiency = 0.85
            self.part_load_curve = lambda plr: np.maximum(0.40, 0.95 * plr**0.8 - 0.15 * (1 - plr)**2)
            
        elif "Boiler" in name:
            self.base_efficiency = 0.88
            self.part_load_curve = lambda plr: np.maximum(0.50, 0.92 * plr**0.75)
            
        elif "Lighting" in name:
            self.base_efficiency = 0.95
            self.part_load_curve = lambda plr: np.full_like(plr, 0.98)
            
        else:  # Fans, Pumps
            self.base_efficiency = 0.75
            self.part_load_curve = lambda plr: np.maximum(0.45, 0.85 * plr**1.1)

    def energy_consumed(self, load_factor: np.ndarray):
        """Calculate energy using part-load efficiency curve."""
        plr = np.asarray(load_factor).copy()
        
        plr = np.maximum(plr, 0.0)           # Only prevent negatives
        # No upper clip needed anymore (your 2.85x peak is fine)
        
        # Get relative efficiency
        relative_efficiency = self.part_load_curve(plr)
        
        # === Improved: Softer minimum power floor ===
        power_draw = self.nominal_power_kw * plr / relative_efficiency
        
        # Optional soft floor (prevents unrealistic zero power)
        #power_draw = np.maximum(power_draw, min_power)
        #min_power = self.nominal_power_kw * 0.015   # 1.5% minimum standby/draw
        energy_kwh = power_draw
        co2_tonnes = energy_kwh * self.co2_factor
        
        return energy_kwh, co2_tonnes

    # ==================== NEW METHOD ====================
    def plot_part_load_curve(self, ax=None):
        """Plot the part-load efficiency curve for this component."""
        if ax is None:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 5))
        
        plr = np.linspace(0.1, 1.2, 200)
        eff = self.part_load_curve(plr)
        
        ax.plot(plr, eff, label=self.name, linewidth=2.5)
        ax.set_xlabel("Part Load Ratio (PLR)")
        ax.set_ylabel("Relative Efficiency")
        ax.set_title(f"Part-Load Efficiency Curve: {self.name}")
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_ylim(0.3, 1.05)
        
        return ax