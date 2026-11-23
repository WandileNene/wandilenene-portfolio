#!/usr/bin/env python
"""
Convenience script for running tests with various options.
Usage: python run_tests.py [options]
"""
import sys
import subprocess
from pathlib import Path


def run_command(cmd):
    """Run a command and return the exit code."""
    print(f"\n{'='*70}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*70}\n")
    # Use python -m for pytest to ensure it works on all platforms
    if cmd[0] == "pytest":
        cmd = ["python", "-m", "pytest"] + cmd[1:]
    elif cmd[0] == "ptw":
        cmd = ["python", "-m", "pytest_watch"] + cmd[1:]
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main test runner with options."""
    # Change to backend directory
    backend_dir = Path(__file__).parent
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--help" or arg == "-h":
            print("""
Portfolio API Test Runner

Usage: python run_tests.py [option]

Options:
  (none)        Run all tests with coverage
  --unit        Run unit tests only
  --integration Run integration tests only
  --fast        Run tests without coverage (faster)
  --coverage    Generate HTML coverage report
  --verbose     Run with verbose output
  --watch       Run in watch mode (requires pytest-watch)
  --help        Show this help message

Examples:
  python run_tests.py                  # Run all tests with coverage
  python run_tests.py --unit           # Run only unit tests
  python run_tests.py --coverage       # Generate HTML coverage report
            """)
            return 0
        
        elif arg == "--unit":
            cmd = ["pytest", "tests/unit/", "-v", "--cov=app", "--cov-report=term-missing"]
        
        elif arg == "--integration":
            cmd = ["pytest", "tests/integration/", "-v", "--cov=app", "--cov-report=term-missing"]
        
        elif arg == "--fast":
            cmd = ["pytest", "-v"]
        
        elif arg == "--coverage":
            cmd = ["pytest", "--cov=app", "--cov-report=html", "--cov-report=term"]
            exit_code = run_command(cmd)
            if exit_code == 0:
                print("\n" + "="*70)
                print("Coverage report generated: htmlcov/index.html")
                print("="*70)
            return exit_code
        
        elif arg == "--verbose":
            cmd = ["pytest", "-vv", "--cov=app", "--cov-report=term-missing"]
        
        elif arg == "--watch":
            try:
                cmd = ["ptw", "--", "--cov=app"]
            except FileNotFoundError:
                print("Error: pytest-watch not installed.")
                print("Install with: pip install pytest-watch")
                return 1
        
        else:
            print(f"Unknown option: {arg}")
            print("Use --help to see available options")
            return 1
    
    else:
        # Default: run all tests with coverage
        cmd = ["pytest", "-v", "--cov=app", "--cov-report=term-missing", "--cov-report=html"]
    
    return run_command(cmd)


if __name__ == "__main__":
    sys.exit(main())
