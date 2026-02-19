#!/usr/bin/env python3
"""
Verification script to check if all assignment requirements are met.
Run this before submission to ensure completeness.
"""

import os
import sys
from pathlib import Path


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text):
    """Print section header."""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}")


def check_file(filepath, description):
    """Check if a file exists."""
    exists = Path(filepath).exists()
    status = f"{Colors.GREEN}✓{Colors.END}" if exists else f"{Colors.RED}✗{Colors.END}"
    print(f"{status} {description}: {filepath}")
    return exists


def check_directory(dirpath, description):
    """Check if a directory exists."""
    exists = Path(dirpath).is_dir()
    status = f"{Colors.GREEN}✓{Colors.END}" if exists else f"{Colors.RED}✗{Colors.END}"
    print(f"{status} {description}: {dirpath}")
    return exists


def check_file_content(filepath, search_string, description):
    """Check if a file contains a specific string."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            found = search_string in content
            status = f"{Colors.GREEN}✓{Colors.END}" if found else f"{Colors.RED}✗{Colors.END}"
            print(f"{status} {description}")
            return found
    except:
        print(f"{Colors.RED}✗{Colors.END} {description} (file error)")
        return False


def main():
    """Run verification checks."""
    print_header("MLOps Assignment 2 - Verification Script")
    print("Group 126\n")
    
    checks_passed = 0
    checks_total = 0
    
    # M1: Model Development & Experiment Tracking
    print_header("M1: Model Development & Experiment Tracking")
    
    checks_total += 1
    if check_file("src/data_preprocessing.py", "Data preprocessing module"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("src/model.py", "Model architecture module"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("src/train.py", "Training script"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_content("src/train.py", "mlflow", "MLflow integration in training"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("data.dvc", "DVC data tracking file"):
        checks_passed += 1
    
    checks_total += 1
    if check_directory(".dvc", "DVC configuration"):
        checks_passed += 1
    
    # M2: Model Packaging & Containerization
    print_header("M2: Model Packaging & Containerization")
    
    checks_total += 1
    if check_file("src/inference.py", "FastAPI inference service"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_content("src/inference.py", "/health", "Health endpoint"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_content("src/inference.py", "/predict", "Prediction endpoint"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("requirements.txt", "Requirements file"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("Dockerfile", "Dockerfile"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("docker-compose.yml", "Docker Compose configuration"):
        checks_passed += 1
    
    # M3: CI Pipeline
    print_header("M3: CI Pipeline for Build, Test & Image Creation")
    
    checks_total += 1
    if check_file("tests/test_preprocessing.py", "Preprocessing unit tests"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("tests/test_model.py", "Model unit tests"):
        checks_passed += 1
    
    checks_total += 1
    if check_file(".github/workflows/ci.yml", "CI pipeline configuration"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_content(".github/workflows/ci.yml", "pytest", "Automated testing in CI"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_content(".github/workflows/ci.yml", "docker", "Docker build in CI"):
        checks_passed += 1
    
    # M4: CD Pipeline & Deployment
    print_header("M4: CD Pipeline & Deployment")
    
    checks_total += 1
    if check_file("deployment/kubernetes/deployment.yaml", "Kubernetes deployment manifest"):
        checks_passed += 1
    
    checks_total += 1
    if check_file(".github/workflows/cd.yml", "CD pipeline configuration"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("tests/smoke_test.py", "Smoke tests"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_content("deployment/kubernetes/deployment.yaml", "livenessProbe", "Health checks in deployment"):
        checks_passed += 1
    
    # M5: Monitoring, Logs & Documentation
    print_header("M5: Monitoring, Logs & Final Submission")
    
    checks_total += 1
    if check_file("src/monitoring.py", "Monitoring module"):
        checks_passed += 1
    
    checks_total += 1
    if check_file_content("src/inference.py", "logging", "Logging in inference service"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("README.md", "README documentation"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("SUBMISSION.md", "Submission guidelines"):
        checks_passed += 1
    
    checks_total += 1
    if check_file(".gitignore", "Git ignore file"):
        checks_passed += 1
    
    # Additional Best Practices
    print_header("Additional Best Practices")
    
    checks_total += 1
    if check_file("QUICKSTART.md", "Quick start guide"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("DATA.md", "Dataset documentation"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("pytest.ini", "Pytest configuration"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("setup.sh", "Setup script"):
        checks_passed += 1
    
    checks_total += 1
    if check_directory("models", "Models directory"):
        checks_passed += 1
    
    checks_total += 1
    if check_directory("logs", "Logs directory"):
        checks_passed += 1
    
    # Summary
    print_header("Verification Summary")
    
    percentage = (checks_passed / checks_total) * 100
    
    print(f"\nChecks Passed: {checks_passed}/{checks_total}")
    print(f"Completion: {percentage:.1f}%\n")
    
    if percentage == 100:
        print(f"{Colors.GREEN}✓ All requirements met! Ready for submission.{Colors.END}")
        return_code = 0
    elif percentage >= 90:
        print(f"{Colors.YELLOW}⚠ Almost complete. Review failed checks above.{Colors.END}")
        return_code = 0
    else:
        print(f"{Colors.RED}✗ Missing requirements. Please complete failed checks.{Colors.END}")
        return_code = 1
    
    print("\nNote: This script checks for file existence, not correctness.")
    print("Make sure to:")
    print("1. Train the model (python src/train.py)")
    print("2. Run tests (pytest tests/ -v)")
    print("3. Test Docker locally (docker-compose up)")
    print("4. Create screen recording")
    print("5. Review SUBMISSION.md for final checklist")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    sys.exit(return_code)


if __name__ == '__main__':
    main()
