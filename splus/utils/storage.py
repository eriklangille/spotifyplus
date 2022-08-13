import os
from pathlib import Path

def get_storage_location():
  storage = (Path.home() / '.splus')
  storage.mkdir(parents=True, exist_ok=True)
  return storage
