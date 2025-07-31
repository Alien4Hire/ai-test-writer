import json
from pathlib import Path

TRACK_FILE = Path("tested_files.json")

# Load tested files from JSON
def load_tested_files():
    if TRACK_FILE.exists():
        return json.loads(TRACK_FILE.read_text())
    return []

# Save tested files
def save_tested_files(tested_files):
    TRACK_FILE.write_text(json.dumps(tested_files, indent=2))

# Add file to tested list
def mark_as_tested(file_path):
    tested = load_tested_files()
    if file_path not in tested:
        tested.append(file_path)
        save_tested_files(tested)
