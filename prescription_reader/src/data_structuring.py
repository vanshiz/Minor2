# data_io.py
import json

def load_text(file_path):
    """Load text from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def save_json(data, file_path):
    """Save data as a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
