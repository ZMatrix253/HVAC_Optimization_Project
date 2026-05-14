import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


def load_from_epw(
    epw_path: str,
    building_params: Dict[str, Any] = None,
    target_year: Optional[int] = None,   # None = use full TMYx (recommended)
) -> Tuple[np.ndarray, np.ndarray]:
    """Load Ottawa TMYx EPW file and calculate hourly load factors.
    
    Returns total load factor and cooling-only load factor.
    """
    if building_params is None:
        building_params = {}

    # Default building parameters
    defaults = {
        'heating_setpoint': 18.0,
        'cooling_setpoint': 24.0,
        'heating_sensitivity': 1.45,
        'cooling_sensitivity': 1.1,
        'solar_factor': 0.012,
        'internal_load_kW': 12.0,
        'area_m2': 2000.0,
        'load_normalization_factor': 1.25
    }
    params = {**defaults, **building_params}

    path = Path(epw_path)
    if not path.exists():
        raise FileNotFoundError(f"EPW file not found: {path}")

    # Read EPW file
    df = pd.read_csv(
        path,
        skiprows=8,
        header=None,
        usecols=[0, 1, 2, 3, 6, 13],
        names=['year', 'month', 'day', 'hour', 'dry_bulb', 'glob_horiz'],
        dtype={'year': int}
    )

    # Clean data
    df['dry_bulb'] = pd.to_numeric(df['dry_bulb'], errors='coerce')
    df['glob_horiz'] = pd.to_numeric(df['glob_horiz'], errors='coerce').fillna(0)

    # Show year distribution in the TMYx file
    print("\n=== Year Contribution in this TMYx File ===")
    print(df['year'].value_counts().sort_values(ascending=False))
    print(f"Total hours in file: {len(df)}\n")

    # Year selection
    if target_year is not None:
        available_years = df['year'].unique()
        if target_year not in available_years:
            raise ValueError(f"Year {target_year} not found. Available: {sorted(available_years)}")

        year_df = df[df['year'] == target_year].copy()
        hours = len(year_df)
        print(f"Using {target_year} data → {hours} hours")
        if hours < 8760:
            print(f"Warning: Year {target_year} is incomplete ({hours}/8760 hours).")
        df = year_df
    else:
        print("Using full TMYx (8760 hours)")

    # Physics-based load calculation
    heating_load = np.maximum(params['heating_setpoint'] - df['dry_bulb'], 0) * params['heating_sensitivity']
    cooling_load = np.maximum(df['dry_bulb'] - params['cooling_setpoint'], 0) * params['cooling_sensitivity']
    solar_gain = df['glob_horiz'] * params['solar_factor']

    total_load = heating_load + cooling_load + solar_gain + params['internal_load_kW']
    cooling_load_only = cooling_load + solar_gain + params['internal_load_kW']

    # Normalize to get load factors
    mean_total = total_load.mean()
    load_factor = total_load.values / mean_total * params['load_normalization_factor']
    cooling_load_factor = cooling_load_only.values / mean_total * params['load_normalization_factor']

    print(f"Loaded {path.name} | Hours: {len(load_factor)} | "
          f"Mean LF: {load_factor.mean():.3f} | Peak: {load_factor.max():.2f}x\n")

    return load_factor, cooling_load_factor