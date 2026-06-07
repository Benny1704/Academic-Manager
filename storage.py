import json
from pathlib import Path

def load_json(filepath):
  path = Path(filepath)

  if not path.exists() or path.stat().st_size == 0:
    return []

  with open(filepath, "r") as file:
    return json.load(file)
  
def save_json(filepath, data):
  with open(filepath, "w") as file:
    json.dump(data, file, indent=4)