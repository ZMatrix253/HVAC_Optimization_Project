# src/config.py
from pathlib import Path
import yaml
from typing import Dict, Any

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load and validate configuration."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    required_sections = ["weather", "building", "constants", "components", "scenarios"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing section '{section}' in config.yaml")

    return config