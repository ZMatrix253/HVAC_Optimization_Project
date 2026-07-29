# Validation against real ASHRAE Great Energy Predictor III dataset
"""
Validation with ASHRAE GEPIII – proper size-normalized (kWh/m²) comparison
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd

from src.hvac_components import HVACComponent
from src.simulation import simulate_hvac
from src.weather import load_from_epw
from src.config import load_config   # use the same config as main.py


print("=== Validation with Real ASHRAE Building Data ===\n")

# ------------------- Load project config -------------------
config = load_config("config.yaml")
building_params = config["building"]
model_area_m2 = building_params.get("area_m2", 2000.0)

# ------------------- Run Your Simulation -------------------
hourly_load, _ = load_from_epw(
    epw_path=config["weather"]["epw_path"],
    building_params=building_params,          # <-- now uses config values
    target_year=config["weather"].get("target_year"),
)

components = [
    HVACComponent(name, power)
    for name, power in config["components"]["baseline"].items()
]

sim_energy, _ = simulate_hvac(components, hourly_load)
sim_annual = float(np.sum(sim_energy))
sim_intensity = sim_annual / model_area_m2

print(f"Your Simulation")
print(f"  Area (declared)     : {model_area_m2:.0f} m²")
print(f"  Annual energy       : {sim_annual:,.0f} kWh")
print(f"  Energy intensity    : {sim_intensity:,.1f} kWh/m²\n")

# ------------------- Load ASHRAE Data -------------------
ashrae = pd.read_csv("data/train.csv")
metadata = pd.read_csv("data/building_metadata.csv")

offices = metadata[metadata["primary_use"] == "Office"].copy()
offices["floor_area_m2"] = offices["square_feet"] * 0.092903

# Similar size band
similar = offices[
    (offices["floor_area_m2"] >= 1500) & (offices["floor_area_m2"] <= 3000)
].copy()

print(f"Found {len(similar)} office buildings with similar size (1500–3000 m²)\n")

if len(similar) == 0:
    print("No close size match – falling back to all offices.")
    similar = offices

# Optional: average the first N matches (more robust than a single building)
N = min(5, len(similar))          # change to 1 if you prefer a single building
selected = similar.head(N)

intensities = []
details = []

for _, row in selected.iterrows():
    bid = int(row["building_id"])
    area = row["floor_area_m2"]

    bdata = ashrae[ashrae["building_id"] == bid]
    elec = bdata[bdata["meter"] == 0]["meter_reading"].sum()

    if area > 0 and elec > 0:
        intensity = elec / area
        intensities.append(intensity)
        details.append({
            "building_id": bid,
            "area_m2": area,
            "annual_kWh": elec,
            "intensity_kWh_m2": intensity,
        })

if not intensities:
    raise RuntimeError("No usable electricity data found for the selected buildings.")

real_intensity_mean = float(np.mean(intensities))
real_intensity_std = float(np.std(intensities)) if len(intensities) > 1 else 0.0

print("Selected ASHRAE building(s):")
for d in details:
    print(f"  ID {d['building_id']:>5}  |  {d['area_m2']:,.0f} m²  |  "
          f"{d['annual_kWh']:,.0f} kWh  |  {d['intensity_kWh_m2']:.1f} kWh/m²")
print(f"\nMean real intensity     : {real_intensity_mean:,.1f} kWh/m²"
      + (f"  (±{real_intensity_std:.1f})" if real_intensity_std else ""))

# ------------------- Size-normalized comparison -------------------
diff_pct = (sim_intensity - real_intensity_mean) / real_intensity_mean * 100

print("\n=== Size-Normalized Comparison (kWh/m²) ===")
print(f"Model intensity         : {sim_intensity:,.1f} kWh/m²")
print(f"ASHRAE mean intensity   : {real_intensity_mean:,.1f} kWh/m²")
print(f"Difference              : {diff_pct:+.1f}%")

print("\nNotes / limitations:")
print("  • Model treats boiler as electric; ASHRAE meter 0 is electricity only.")
print("  • Ottawa TMYx weather vs. unknown climates of the ASHRAE sites.")
print("  • area_m2 is currently only a label – load does not scale with it.")
print("  • This is a high-level reasonableness check, not a formal calibration.")

# ------------------- Save results -------------------
Path("validation").mkdir(exist_ok=True)

summary = pd.DataFrame({
    "Metric": [
        "Model area (m²)",
        "Model annual energy (kWh)",
        "Model intensity (kWh/m²)",
        "ASHRAE mean intensity (kWh/m²)",
        "ASHRAE intensity std (kWh/m²)",
        "Difference (%)",
        "Number of ASHRAE buildings averaged",
    ],
    "Value": [
        model_area_m2,
        sim_annual,
        sim_intensity,
        real_intensity_mean,
        real_intensity_std,
        diff_pct,
        len(intensities),
    ],
})
summary.to_csv("validation/ashrae_comparison.csv", index=False)

pd.DataFrame(details).to_csv("validation/ashrae_buildings_used.csv", index=False)

print("\nResults saved to:")
print("  validation/ashrae_comparison.csv")
print("  validation/ashrae_buildings_used.csv")