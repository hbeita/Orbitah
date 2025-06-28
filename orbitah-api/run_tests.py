#!/usr/bin/env python3
"""
Test runner script that runs each test file using the dedicated PostgreSQL test database.
"""

import glob
import os
import subprocess
import sys


def run_tests():
    """Run all test files using PostgreSQL test database"""
    test_files = glob.glob("tests/test_*.py")
    test_files.sort()

    total_passed = 0
    total_failed = 0

    print("Running tests with dedicated PostgreSQL test database...")
    print("=" * 60)

    for test_file in test_files:
        print(f"\nRunning {test_file}...")

        # Run the test file with PostgreSQL test database
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", test_file, "-v",
                "--tb=short"
            ],
            env={
                **os.environ,
                "TEST_DATABASE_URL": "postgresql+psycopg2://orbitah_test:orbitah_test_password@localhost:5434/orbitah_test_db"
            },
            capture_output=True,
            text=True,
            timeout=60
            )

            if result.returncode == 0:
                print(f"✅ {test_file} - PASSED")
                total_passed += 1
            else:
                print(f"❌ {test_file} - FAILED")
                print(result.stdout)
                print(result.stderr)
                total_failed += 1

        except subprocess.TimeoutExpired:
            print(f"❌ {test_file} - TIMEOUT")
            total_failed += 1
        except Exception as e:
            print(f"❌ {test_file} - ERROR: {e}")
            total_failed += 1

    print("\n" + "=" * 60)
    print(f"SUMMARY: {total_passed} passed, {total_failed} failed")

    if total_failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"💥 {total_failed} test files failed!")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
