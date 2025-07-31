import subprocess
from pathlib import Path

# Recursively search upward for the closest directory containing package.json
def find_package_json_dir(start_path: Path) -> Path | None:
    current = start_path.resolve()
    for parent in [current] + list(current.parents):
        if (parent / 'package.json').exists():
            return parent
    return None

# Run tests in the correct directory
def run_tests(source_file_path: str):
    test_dir = Path(source_file_path).parent
    package_dir = find_package_json_dir(test_dir)

    if not package_dir:
        return 1, '', f'❌ No package.json found near {source_file_path}'

    try:
        result = subprocess.run(
            'npm test',
            cwd=str(package_dir),
            shell=True,
            text=True,
            check=False
        )
        return result.returncode, '', ''
    except subprocess.TimeoutExpired:
        return 1, '', '❌ Test runner timed out.'
    except Exception as e:
        return 1, '', f'❌ Test runner failed: {str(e)}'
