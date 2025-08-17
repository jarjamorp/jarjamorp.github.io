from pathlib import Path
import yaml

def load_config(config_path: str | None = None) -> dict:
    p = Path(config_path or "config.yml")
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
