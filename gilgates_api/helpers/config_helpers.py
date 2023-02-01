from typing import Dict
import tomli


def get_project_metadata(base_dir: str) -> Dict[str, str]:
    with open(f"{base_dir}/pyproject.toml", "rb") as f:
        data = tomli.load(f)
    return data["tool"]["poetry"]
