import subprocess
from pathlib import Path
import shutil
import json

def find_package_json_dir(start_path: Path) -> Path | None:
    current = start_path.resolve()
    for parent in [current] + list(current.parents):
        if (parent / 'package.json').exists():
            return parent
    return None

def run_tests(source_file_path: str, timeout_seconds: int = 30):
    print(f"🔍 Locating package.json starting from: {source_file_path}")
    test_dir = Path(source_file_path).parent
    package_dir = find_package_json_dir(test_dir)

    if not package_dir:
        error_msg = f'❌ No package.json found near {source_file_path}'
        print(error_msg)
        return 1, '', error_msg

    print(f"📦 Found package.json in: {package_dir}")

    # Find the full path to npm.cmd on Windows
    npm_cmd = shutil.which("npm")
    if not npm_cmd:
        return 1, '', "❌ Could not find `npm` in PATH"

    print(f"🚀 Running `npm test` via {npm_cmd} in {package_dir} (timeout: {timeout_seconds}s)")

    try:
        result = subprocess.run(
            [npm_cmd, "test"],
            cwd=str(package_dir),
            shell=False,
            text=True,
            timeout=timeout_seconds
        )
        print(f"✅ npm test exited with code {result.returncode}")
        return result.returncode, '', ''
    except subprocess.TimeoutExpired:
        return 1, '', f'⏳ npm test timed out after {timeout_seconds}s'
    except Exception as e:
        return 1, '', f'❌ npm test failed: {e}'
    
def run_tests_and_get_coverage(source_file_path: str, timeout_seconds: int = 60) -> tuple[int, bool]:
    test_dir = Path(source_file_path).parent
    package_dir = find_package_json_dir(test_dir)

    if not package_dir:
        print(f"⚠️ Could not find package.json for coverage check.")
        return 9999, False

    coverage_output = package_dir / "coverage" / "coverage-final.json"
    print(f"📊 Running coverage via `npm run coverage` for: {source_file_path}")

    # Locate npm command (handles Windows too)
    npm_cmd = shutil.which("npm")
    if not npm_cmd:
        print("❌ Could not find `npm` in PATH")
        return 9999, False

    try:
        # Run the user's coverage script
        result = subprocess.run(
            [npm_cmd, "run", "coverage"],
            cwd=str(package_dir),
            shell=False,
            text=True,
            timeout=timeout_seconds
        )

        passed = result.returncode == 0

        if not coverage_output.exists():
            print(f"⚠️ Coverage file not found at {coverage_output}")
            return 9999, passed

        # Parse and check coverage data
        coverage_data = json.loads(coverage_output.read_text())
        source_path = Path(source_file_path).resolve()
        coverage_keys = [Path(k).resolve() for k in coverage_data.keys()]

        for key_path, key in zip(coverage_keys, coverage_data.keys()):
            if key_path == source_path:
                file_coverage = coverage_data[key]
                uncovered = sum(1 for hits in file_coverage["s"].values() if hits == 0)
                print(f"✅ Uncovered lines for {key}: {uncovered}")
                return uncovered, passed

        print(f"⚠️ No matching coverage key for {source_path}")
        for k in coverage_data.keys():
            print(f"  - {k}")

        return 9999, passed

    except subprocess.TimeoutExpired:
        print("⏰ npm run coverage timed out.")
        return 9999, False
    except Exception as e:
        print(f"❌ Failed to run coverage: {e}")
        return 9999, False
