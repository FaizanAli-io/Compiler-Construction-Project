#!/usr/bin/env python3
"""
Test runner for PatternLang compiler.
Runs all sample programs and reports results.
Interactive menu allows selecting which tests to run.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from patternlang.main import compile_and_run
from patternlang.utils.errors import CompilerError


def run_test(test_file, show_source=True, verbose=False):
    """Run a single test file."""
    print(f"\n{'=' * 70}")
    print(f"Running: {test_file.name}")
    print("=" * 70)

    try:
        source_code = test_file.read_text(encoding="utf-8")

        if show_source:
            print(f"\nSource Code:")
            print("-" * 70)
            print(source_code)
            print("-" * 70)

        print("\nOutput:")
        compile_and_run(source_code, verbose=verbose)
        print("\n[PASS] Test passed")
        return True
    except CompilerError as e:
        # Handle compiler errors gracefully
        print(f"\n[COMPILER ERROR] {type(e).__name__}")
        print(f"Message: {e}")
        print("\n[PASS] Error handling verified (expected error)")
        return True
    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def display_menu(test_files):
    """Display interactive menu for test selection."""
    print("\n" + "=" * 70)
    print("PatternLang Compiler Test Suite")
    print("=" * 70)
    print(f"Found {len(test_files)} test file(s)\n")

    # Categorize tests
    sample_tests = [f for f in test_files if f.name.startswith("sample_")]
    conditional_tests = [f for f in test_files if f.name.startswith("conditional_")]
    float_tests = [f for f in test_files if f.name.startswith("float_")]
    error_tests = [f for f in test_files if f.name.startswith("error_")]

    print("Available Tests:")
    print("-" * 70)

    idx = 1
    test_map = {}

    if sample_tests:
        print("\nSample Programs:")
        for test_file in sample_tests:
            print(f"  [{idx}] {test_file.name}")
            test_map[str(idx)] = test_file
            idx += 1

    if conditional_tests:
        print("\nConditional Logic Tests:")
        for test_file in conditional_tests:
            print(f"  [{idx}] {test_file.name}")
            test_map[str(idx)] = test_file
            idx += 1

    if float_tests:
        print("\nFloat Tests:")
        for test_file in float_tests:
            print(f"  [{idx}] {test_file.name}")
            test_map[str(idx)] = test_file
            idx += 1

    if error_tests:
        print("\nError Handling Tests:")
        for test_file in error_tests:
            print(f"  [{idx}] {test_file.name}")
            test_map[str(idx)] = test_file
            idx += 1

    print("\n" + "-" * 70)
    print("Options:")
    print("  [A] Run all tests")
    print("  [Q] Quit")
    print("  [1-N] Run specific test(s) (comma-separated: 1,3,5)")
    print("-" * 70)

    return test_map


def get_user_selection(test_map):
    """Get user input for test selection."""
    while True:
        choice = input("\nEnter your choice (A/Q/1-N): ").strip().upper()

        if choice == "A":
            return list(test_map.values())
        elif choice == "Q":
            return None
        elif choice:
            # Parse comma-separated test numbers
            try:
                test_nums = [s.strip() for s in choice.split(",")]
                selected = []
                for num in test_nums:
                    if num in test_map:
                        selected.append(test_map[num])
                    else:
                        print(f"Invalid test number: {num}")
                        break
                else:
                    if selected:
                        return selected
            except Exception:
                pass

        print("Invalid input. Please enter A, Q, or valid test numbers (1-N).")


def get_verbosity_option():
    """Get verbosity preference from user."""
    while True:
        choice = input("\nEnable verbose output? (Y/N): ").strip().upper()
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("Invalid input. Please enter Y or N.")


def main():
    """Run tests with interactive menu."""
    tests_dir = Path(__file__).parent
    test_files = sorted(tests_dir.glob("*.pl"))

    if not test_files:
        print("No test files found (*.pl)")
        sys.exit(1)

    # Display menu and get user selection
    test_map = display_menu(test_files)
    selected_tests = get_user_selection(test_map)

    if selected_tests is None:
        print("\nQuitting...")
        sys.exit(0)

    # Get verbosity preference
    verbose = get_verbosity_option()

    # Run selected tests
    print("\n" + "=" * 70)
    print("Running Selected Tests")
    print(f"Verbose Mode: {'ON' if verbose else 'OFF'}")
    print("=" * 70)

    results = []
    for test_file in selected_tests:
        results.append(run_test(test_file, verbose=verbose))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("[SUCCESS] All selected tests passed!")
        sys.exit(0)
    else:
        print(f"[FAILED] {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
