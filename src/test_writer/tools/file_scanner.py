import os
from test_writer.tools.test_tracker import load_tested_files

# Check if test file already exists or is marked as tested
def needs_test(file_path):
    tested = load_tested_files()
    if file_path in tested:
        return False
    if file_path.endswith(('.test.js', '.test.ts', '.test.jsx', '.test.tsx')):
        return False
    return True

# Recursively find code files
def find_target_files(folder):
    results = []
    for root, _, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith(('.js', '.ts', '.jsx', '.tsx')) and needs_test(full_path):
                results.append(full_path)
    return results
