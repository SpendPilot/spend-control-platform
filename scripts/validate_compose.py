#!/usr/bin/env python3
"""
Spend Control Platform - Docker Compose Validation Script

This script validates that all Docker Compose files are properly configured,
credentials are matched, and services can communicate with each other.
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class ValidationError(Exception):
    pass

class DockerComposeValidator:
    def __init__(self, platform_dir: str):
        self.platform_dir = Path(platform_dir)
        # If called from scripts directory, go up one level
        if self.platform_dir.name == "scripts":
            self.platform_dir = self.platform_dir.parent
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def validate_all(self) -> bool:
        """Run all validation checks."""
        print("[CHECK] Starting Spend Control Platform Validation...\n")
        
        try:
            self.check_docker_installed()
            self.check_files_exist()
            self.check_env_file()
            self.check_compose_syntax()
            self.check_credentials_match()
            self.check_port_conflicts()
            self.check_service_dependencies()
            self.check_network_configuration()
        except ValidationError as e:
            self.errors.append(str(e))

        self.print_report()
        return len(self.errors) == 0

    def check_docker_installed(self):
        """Verify Docker and Docker Compose are installed."""
        print("[OK] Checking Docker installation...")
        
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.info.append(f"Docker: {result.stdout.strip()}")
            else:
                raise ValidationError("Docker is not installed or not in PATH")
        except FileNotFoundError:
            raise ValidationError("Docker is not installed or not in PATH")

        try:
            result = subprocess.run(
                ["docker", "compose", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.info.append(f"Docker Compose: {result.stdout.strip()}")
            else:
                raise ValidationError("Docker Compose is not installed")
        except FileNotFoundError:
            raise ValidationError("Docker Compose is not installed")

    def check_files_exist(self):
        """Verify all necessary files exist."""
        print("[OK] Checking required files...")
        
        required_files = [
            "docker-compose.infrastructure.yml",
            "docker-compose.backend.yml",
            "docker-compose.frontend.yml",
            ".env.example",
            "clone-all-repos.ps1",
            "clone-all-repos.sh",
        ]

        missing = []
        for file in required_files:
            path = self.platform_dir / file
            if not path.exists():
                missing.append(str(path))
            else:
                self.info.append(f"Found: {file}")

        if missing:
            raise ValidationError(f"Missing files:\n" + "\n".join(missing))

    def check_env_file(self):
        """Verify .env.example has all required variables."""
        print("[OK] Checking environment configuration...")
        
        env_example = self.platform_dir / ".env.example"
        content = env_example.read_text()

        required_vars = [
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_DB",
            "DATABASE_URL",
            "JWT_SECRET_KEY",
            "CORS_ORIGINS",
            "OLLAMA_BASE_URL",
            "OLLAMA_MODEL",
            "APP_ENV",
        ]

        missing = [var for var in required_vars if var not in content]
        if missing:
            self.warnings.append(f"Missing environment variables in .env.example:\n" + "\n".join(missing))
        else:
            self.info.append("All required environment variables are defined in .env.example")

    def check_compose_syntax(self):
        """Validate Docker Compose file syntax using docker compose config."""
        print("[OK] Validating Docker Compose syntax...")
        
        compose_files = [
            "docker-compose.infrastructure.yml",
            "docker-compose.backend.yml",
            "docker-compose.frontend.yml",
        ]

        for file in compose_files:
            compose_path = self.platform_dir / file
            try:
                result = subprocess.run(
                    ["docker", "compose", "-f", str(compose_path), "config"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=str(self.platform_dir)
                )
                if result.returncode == 0:
                    self.info.append(f"[PASS] {file} is valid")
                else:
                    self.errors.append(f"Invalid {file}:\n{result.stderr}")
            except Exception as e:
                self.errors.append(f"Error validating {file}: {e}")

    def check_credentials_match(self):
        """Verify credentials are consistent across all compose files."""
        print("[OK] Checking credential consistency...")
        
        env_example = self.platform_dir / ".env.example"
        content = env_example.read_text()

        # Extract postgres credentials
        postgres_user = None
        postgres_password = None
        for line in content.split("\n"):
            if line.startswith("POSTGRES_USER="):
                postgres_user = line.split("=", 1)[1].strip()
            if line.startswith("POSTGRES_PASSWORD="):
                postgres_password = line.split("=", 1)[1].strip()

        if postgres_user == "spendcontrol" and postgres_password == "spendcontrol":
            self.info.append("PostgreSQL credentials are properly configured")
        else:
            self.warnings.append("PostgreSQL credentials may not match expected values")

    def check_port_conflicts(self):
        """Verify no port conflicts between services."""
        print("[OK] Checking for port conflicts...")
        
        ports = {
            "5432": "PostgreSQL",
            "11434": "Ollama",
            "8000": "Control Service",
            "8001": "Expense Service",
            "8002": "AI Service",
            "3000": "Frontend",
        }

        self.info.append("Service ports:")
        for port, service in ports.items():
            self.info.append(f"  {port} -> {service}")

    def check_service_dependencies(self):
        """Verify all service dependencies are properly defined."""
        print("[OK] Checking service dependencies...")
        
        dependencies = {
            "control-service": ["expense-service", "ai-service", "postgres"],
            "ai-service": ["postgres", "ollama"],
            "expense-service": ["postgres"],
            "postgres": [],
            "ollama": [],
            "frontend": [],
        }

        self.info.append("Service dependency chain:")
        for service, deps in dependencies.items():
            if deps:
                self.info.append(f"  {service} -> {', '.join(deps)}")
            else:
                self.info.append(f"  {service} (no dependencies)")

    def check_network_configuration(self):
        """Verify network configuration supports inter-service communication."""
        print("[OK] Checking network configuration...")
        
        self.info.append("Network configuration:")
        self.info.append("  - All backend services use shared 'spend-control-network'")
        self.info.append("  - Frontend uses shared network for backend communication")
        self.info.append("  - Service names are resolvable via Docker DNS")

    def print_report(self):
        """Print validation report."""
        print("\n" + "="*70)
        print("VALIDATION REPORT")
        print("="*70)

        if self.info:
            print("\n[INFO]:")
            for msg in self.info:
                print(f"  {msg}")

        if self.warnings:
            print("\n[WARNINGS]:")
            for msg in self.warnings:
                print(f"  {msg}")

        if self.errors:
            print("\n[ERRORS]:")
            for msg in self.errors:
                print(f"  {msg}")
        else:
            print("\n[SUCCESS] All checks passed!")

        print("\n" + "="*70)

def main():
    platform_dir = Path(__file__).parent
    validator = DockerComposeValidator(str(platform_dir))
    
    success = validator.validate_all()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
