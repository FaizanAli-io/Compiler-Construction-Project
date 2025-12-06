"""
Test assembly code generation for PatternLang compiler.
Generates assembly files for all test programs.
"""

import sys
import subprocess
from pathlib import Path


def test_assembly_generation():
    """Generate assembly for all test programs."""
    tests_dir = Path("tests")
    outputs_dir = Path("outputs")

    # Get all .pl files
    test_files = list(tests_dir.glob("*.pl"))

    print(f"Found {len(test_files)} test programs")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for test_file in sorted(test_files):
        print(f"\nCompiling: {test_file.name}")
        print("-" * 60)

        try:
            # Run compiler with --compile flag
            result = subprocess.run(
                [sys.executable, "main.py", str(test_file), "--compile"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                print(f"[PASS] Success: {result.stdout.strip()}")
                success_count += 1

                # Check if assembly file was created
                asm_file = outputs_dir / f"{test_file.stem}.asm"
                if asm_file.exists():
                    line_count = len(asm_file.read_text().splitlines())
                    print(f"  Assembly file: {line_count} lines")
            else:
                print(f"[FAIL] Failed:")
                print(f"  {result.stderr}")
                fail_count += 1

        except subprocess.TimeoutExpired:
            print(f"[FAIL] Timeout")
            fail_count += 1
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            fail_count += 1

    print("\n" + "=" * 60)
    print(f"Results: {success_count} passed, {fail_count} failed")
    print("=" * 60)

    return fail_count == 0


if __name__ == "__main__":
    success = test_assembly_generation()
    sys.exit(0 if success else 1)
