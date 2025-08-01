import subprocess
from pathlib import Path
import shutil

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
