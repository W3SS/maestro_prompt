#!/usr/bin/env python3
"""
Local CI Test Runner
====================

Runs all CI checks locally before pushing to GitHub.
Mimics the exact same checks that run in GitHub Actions.

Usage:
    python scripts/run_ci_checks.py              # Run all checks
    python scripts/run_ci_checks.py --fast       # Skip slow checks
    python scripts/run_ci_checks.py --fix        # Auto-fix issues
"""

import subprocess
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def run_command(cmd: List[str], description: str, fix_mode: bool = False) -> Tuple[bool, str]:
    """
    Run a command and return success status.
    
    Args:
        cmd: Command to run
        description: Human-readable description
        fix_mode: Whether to attempt auto-fix
    
    Returns:
        Tuple of (success, output)
    """
    print(f"\n{Colors.BLUE}{Colors.BOLD}▶ {description}{Colors.END}")
    print(f"  Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ PASSED{Colors.END}")
            return True, result.stdout
        else:
            print(f"{Colors.RED}✗ FAILED{Colors.END}")
            if result.stderr:
                print(f"{Colors.RED}{result.stderr}{Colors.END}")
            if result.stdout:
                print(result.stdout)
            return False, result.stderr
            
    except Exception as e:
        print(f"{Colors.RED}✗ ERROR: {e}{Colors.END}")
        return False, str(e)


def main():
    """Run all CI checks."""
    parser = argparse.ArgumentParser(description="Run local CI checks")
    parser.add_argument("--fast", action="store_true", help="Skip slow checks")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues when possible")
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Maestro AI - Local CI Test Runner{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    
    checks = []
    results = []
    
    # 1. Install dependencies
    checks.append((
        ["pip", "install", "-r", "requirements.txt", "-q"],
        "Installing dependencies",
        False
    ))
    
    # 2. Lint with Ruff
    if args.fix:
        checks.append((
            ["ruff", "check", "src/", "tests/", "--fix"],
            "Linting with Ruff (auto-fix)",
            True
        ))
    else:
        checks.append((
            ["ruff", "check", "src/", "tests/"],
            "Linting with Ruff",
            False
        ))
    
    # 3. Type check with Mypy
    checks.append((
        ["mypy", "src/", "--ignore-missing-imports"],
        "Type checking with Mypy",
        False
    ))
    
    # 4. Security scan with Bandit
    checks.append((
        ["bandit", "-r", "src/", "-ll"],
        "Security scanning with Bandit",
        False
    ))
    
    # 5. Run tests with coverage
    if args.fast:
        checks.append((
            ["pytest", "tests/unit/", "-v", "--tb=short"],
            "Running unit tests (fast mode)",
            False
        ))
    else:
        checks.append((
            ["pytest", "--cov=src", "--cov-report=term-missing", "--cov-report=html", "-v"],
            "Running tests with coverage",
            False
        ))
    
    # 6. Check coverage threshold
    if not args.fast:
        checks.append((
            ["coverage", "report", "--fail-under=95"],
            "Checking coverage threshold (95%)",
            False
        ))
    
    # Execute all checks
    for cmd, description, is_fix in checks:
        success, output = run_command(cmd, description, is_fix)
        results.append((description, success))
    
    # Summary
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}SUMMARY{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if success else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"{status} - {description}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} checks passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED!{Colors.END}")
        print(f"{Colors.GREEN}Your code is ready to push to GitHub.{Colors.END}")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ SOME CHECKS FAILED{Colors.END}")
        print(f"{Colors.YELLOW}Fix the issues above before pushing.{Colors.END}")
        
        if not args.fix:
            print(f"\n{Colors.YELLOW}Tip: Run with --fix to auto-fix some issues{Colors.END}")
        
        sys.exit(1)


if __name__ == "__main__":
    main()
