#!/usr/bin/env python3
"""
Quick verification script for Assignment 2 reviewers.
Checks if all required files and configurations are present.
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


def check_file(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"{Colors.GREEN}✓{Colors.END} {description}: {filepath}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.END} {description} MISSING: {filepath}")
        return False


def check_directory(dirpath, description):
    """Check if a directory exists."""
    if Path(dirpath).is_dir():
        print(f"{Colors.GREEN}✓{Colors.END} {description}: {dirpath}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.END} {description} MISSING: {dirpath}")
        return False


def count_tests(test_dir):
    """Count test files."""
    test_files = list(Path(test_dir).glob("test_*.py"))
    return len(test_files)


def main():
    print("=" * 70)
    print(f"{Colors.BLUE}MLOps Assignment 2 - Verification Checklist{Colors.END}")
    print("=" * 70)
    
    checks_passed = 0
    checks_total = 0
    
    # Module 1: Model Development & Experiment Tracking
    print(f"\n{Colors.BLUE}[M1] Model Development & Experiment Tracking{Colors.END}")
    print("-" * 70)
    
    checks_total += 1
    if check_file("src/model.py", "Model architecture"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("src/train.py", "Training script"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("data.dvc", "DVC data tracking"):
        checks_passed += 1
    
    checks_total += 1
    if check_directory(".dvc", "DVC configuration"):
        checks_passed += 1
    
    # Check MLflow integration in train.py
    checks_total += 1
    if Path("src/train.py").exists():
        with open("src/train.py", "r") as f:
            content = f.read()
            if "mlflow" in content.lower():
                print(f"{Colors.GREEN}✓{Colors.END} MLflow integration found in train.py")
                checks_passed += 1
            else:
                print(f"{Colors.RED}✗{Colors.END} MLflow integration NOT found in train.py")
    
    # Module 2: Model Packaging & Containerization
    print(f"\n{Colors.BLUE}[M2] Model Packaging & Containerization{Colors.END}")
    print("-" * 70)
    
    checks_total += 1
    if check_file("src/inference.py", "FastAPI inference service"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("Dockerfile", "Docker configuration"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("docker-compose.yml", "Docker Compose configuration"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("requirements.txt", "Python dependencies"):
        checks_passed += 1
    
    # Check for required endpoints
    checks_total += 1
    if Path("src/inference.py").exists():
        with open("src/inference.py", "r") as f:
            content = f.read()
            if "/health" in content and "/predict" in content:
                print(f"{Colors.GREEN}✓{Colors.END} API endpoints (/health, /predict) found")
                checks_passed += 1
            else:
                print(f"{Colors.RED}✗{Colors.END} Required API endpoints NOT found")
    
    # Module 3: CI Pipeline
    print(f"\n{Colors.BLUE}[M3] CI Pipeline{Colors.END}")
    print("-" * 70)
    
    checks_total += 1
    if check_directory("tests", "Tests directory"):
        checks_passed += 1
        num_tests = count_tests("tests")
        print(f"  {Colors.YELLOW}→{Colors.END} Found {num_tests} test file(s)")
    
    checks_total += 1
    if check_file(".github/workflows/ci.yml", "CI workflow"):
        checks_passed += 1
    
    # Check for pytest configuration
    checks_total += 1
    if check_file("setup.cfg", "Test configuration (setup.cfg)"):
        checks_passed += 1
    
    # Module 4: CD Pipeline & Deployment
    print(f"\n{Colors.BLUE}[M4] CD Pipeline & Deployment{Colors.END}")
    print("-" * 70)
    
    checks_total += 1
    if check_file(".github/workflows/cd.yml", "CD workflow"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("deployment/kubernetes/deployment.yaml", "Kubernetes manifests"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("tests/smoke_test.py", "Smoke tests"):
        checks_passed += 1
    
    # Module 5: Monitoring & Logging
    print(f"\n{Colors.BLUE}[M5] Monitoring & Logging{Colors.END}")
    print("-" * 70)
    
    checks_total += 1
    if check_file("src/monitoring.py", "Monitoring module"):
        checks_passed += 1
    
    # Check for logging in inference.py
    checks_total += 1
    if Path("src/inference.py").exists():
        with open("src/inference.py", "r") as f:
            content = f.read()
            if "logging" in content:
                print(f"{Colors.GREEN}✓{Colors.END} Logging configured in inference.py")
                checks_passed += 1
            else:
                print(f"{Colors.RED}✗{Colors.END} Logging NOT found in inference.py")
    
    # Additional checks
    print(f"\n{Colors.BLUE}[Additional Files]{Colors.END}")
    print("-" * 70)
    
    checks_total += 1
    if check_file("README.md", "Project documentation"):
        checks_passed += 1
    
    checks_total += 1
    if check_file(".gitignore", "Git ignore file"):
        checks_passed += 1
    
    checks_total += 1
    if check_file("Makefile", "Makefile (optional)"):
        checks_passed += 1
    
    # Summary
    print("\n" + "=" * 70)
    percentage = (checks_passed / checks_total) * 100
    
    if percentage == 100:
        print(f"{Colors.GREEN}✓ All checks passed! ({checks_passed}/{checks_total}){Colors.END}")
        print(f"{Colors.GREEN}Project structure is complete.{Colors.END}")
    elif percentage >= 80:
        print(f"{Colors.YELLOW}⚠ Most checks passed ({checks_passed}/{checks_total} - {percentage:.1f}%){Colors.END}")
        print(f"{Colors.YELLOW}Review missing items above.{Colors.END}")
    else:
        print(f"{Colors.RED}✗ Several checks failed ({checks_passed}/{checks_total} - {percentage:.1f}%){Colors.END}")
        print(f"{Colors.RED}Please review the missing components.{Colors.END}")
    
    print("=" * 70)
    
    # Next steps
    print(f"\n{Colors.BLUE}Next Steps:{Colors.END}")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Download dataset: kaggle competitions download -c dogs-vs-cats")
    print("3. Prepare dataset: python src/prepare_dataset.py --source train --output data")
    print("4. Train model: python src/train.py --epochs 5")
    print("5. Run tests: pytest tests/ -v")
    print("6. Build Docker: docker build -t cats-dogs-classifier:latest .")
    print("7. Deploy to K8s: kubectl apply -f deployment/kubernetes/deployment.yaml")
    
    return 0 if percentage == 100 else 1


if __name__ == "__main__":
    sys.exit(main())
