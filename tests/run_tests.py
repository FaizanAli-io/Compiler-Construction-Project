#!/usr/bin/env python3
"""
Test runner for PatternLang compiler.
Runs all sample programs and reports results.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from patternlang.main import compile_and_run


def run_test(test_file):
    """Run a single test file."""
    print(f"\n{'=' * 70}")
    print(f"Running: {test_file.name}")
    print("=" * 70)

    try:
        source_code = test_file.read_text(encoding="utf-8")
        print(f"\nSource Code:")
        print("-" * 70)
        print(source_code)
        print("-" * 70)
        print("\nOutput:")
        compile_and_run(source_code, verbose=False)
        print("\n✓ Test passed")
        return True
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    tests_dir = Path(__file__).parent
    test_files = sorted(tests_dir.glob("*.pl"))

    if not test_files:
        print("No test files found (*.pl)")
        sys.exit(1)

    print("=" * 70)
    print("PatternLang Compiler Test Suite")
    print("=" * 70)
    print(f"Found {len(test_files)} test file(s)")

    results = []
    for test_file in test_files:
        results.append(run_test(test_file))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"✗ {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
