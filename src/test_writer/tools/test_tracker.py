import json
from pathlib import Path

TRACK_FILE = Path("tested_files.json")

# Load tested files from JSON
def load_tested_files():
    if TRACK_FILE.exists():
        return json.loads(TRACK_FILE.read_text())
    return []

def save_tested_files(tested_files):
    TRACK_FILE.write_text(json.dumps(tested_files, indent=2))

def mark_as_tested(entry):
    tested = load_tested_files()
    if not any(f["path"] == entry["path"] for f in tested):
        tested.append(entry)
        save_tested_files(tested)

