import json
from pathlib import Path
from enum import Enum

def load_json(filepath):
  path = Path(filepath)

  if not path.exists() or path.stat().st_size == 0:
    return []

  with open(filepath, "r", encoding="utf-8") as file:
    return json.load(file)
  
def _normalize_for_json(value):
  if isinstance(value, Enum):
    return value.value
  if isinstance(value, dict):
    return {key: _normalize_for_json(val) for key, val in value.items()}
  if isinstance(value, list):
    return [_normalize_for_json(item) for item in value]
  return value

def save_json(filepath, data):
  with open(filepath, "w", encoding="utf-8") as file:
    json.dump(_normalize_for_json(data), file, indent=4)