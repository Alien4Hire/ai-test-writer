import json
from pathlib import Path

TRACK_FILE = Path("tested_files.json")

# Load tested files from JSON
def load_tested_files():
    if TRACK_FILE.exists():
        return json.loads(TRACK_FILE.read_text())
    return []

def get_logged_coverage(file_path: str) -> int | None:
    tested = load_tested_files()
    for f in tested:
        if f["path"] == file_path and "uncovered_lines" in f:
            return f["uncovered_lines"]
    return None

# Check if file has been marked as tested
def is_tested(file_path: str):
    tested = load_tested_files()
    return any(f["path"] == file_path for f in tested)

def save_tested_files(tested_files):
    TRACK_FILE.write_text(json.dumps(tested_files, indent=2))

def mark_as_tested(entry):
    tested = load_tested_files()
    # Replace old entry if it exists
    tested = [f for f in tested if f["path"] != entry["path"]]
    tested.append(entry)
    save_tested_files(tested)

