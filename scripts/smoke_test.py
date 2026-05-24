from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = ROOT.parent / "spend-control-frontend"
CONTROL_ROOT = ROOT.parent / "spend-control-control-service"
EXPENSE_ROOT = ROOT.parent / "spend-control-expense-service"
AI_ROOT = ROOT.parent / "spend-control-ai-service"
DEFAULT_SMOKE_ENV = {
    "APP_ENV": "development",
    "DATABASE_URL": "postgresql+psycopg://spendcontrol:spendcontrol@localhost:5432/spend_control",
    "CORS_ORIGINS": "http://localhost:3000",
    "JWT_SECRET_KEY": "dev-secret-change-me",
    "EXPENSE_SERVICE_URL": "http://localhost:8001",
    "AI_SERVICE_URL": "http://localhost:8002",
    "UPLOAD_DIR": str(ROOT / ".smoke-uploads"),
    "OLLAMA_BASE_URL": "http://localhost:11434",
    "OLLAMA_MODEL": "llama3.2",
    "OLLAMA_REQUEST_TIMEOUT": "30",
    "RECEIPT_REQUIRED_THRESHOLD": "75",
    "NEXT_PUBLIC_API_BASE_URL": "http://localhost:8000",
}


def run(
    command: list[str],
    cwd: Path | None = None,
    allow_failure: bool = False,
    env: dict[str, str] | None = None,
) -> None:
    if os.name == "nt" and command[0] == "npm":
        command = ["npm.cmd", *command[1:]]
    result = subprocess.run(command, cwd=cwd or ROOT, check=False, text=True, env=env)
    if result.returncode != 0 and not allow_failure:
        raise RuntimeError(f"Command failed: {' '.join(command)}")


def check_url(url: str, optional: bool = False) -> None:
    try:
        with urlopen(url, timeout=5) as response:
            print(f"{url}: {response.status}")
    except URLError:
        if optional:
            print(f"{url}: unavailable (optional)")
            return
        raise


def main() -> None:
    smoke_env = os.environ.copy()
    smoke_env.update(DEFAULT_SMOKE_ENV)
    Path(smoke_env["UPLOAD_DIR"]).mkdir(parents=True, exist_ok=True)

    print("Checking backend imports...")
    run([sys.executable, "-c", "import app.main"], cwd=CONTROL_ROOT, env=smoke_env)
    run([sys.executable, "-c", "import app.main"], cwd=EXPENSE_ROOT, env=smoke_env)
    run([sys.executable, "-c", "import app.main"], cwd=AI_ROOT, env=smoke_env)

    print("Checking frontend build capability...")
    if (FRONTEND_ROOT / "node_modules").exists():
        run(["npm", "run", "build"], cwd=FRONTEND_ROOT, allow_failure=False, env=smoke_env)
    else:
        print("node_modules missing: skipped frontend build")

    print("Checking health endpoints...")
    for url in [
        "http://localhost:8000/health",
        "http://localhost:8001/health",
        "http://localhost:8002/health",
    ]:
        check_url(url, optional=True)

    print("Checking Ollama connectivity...")
    ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    check_url(f"{ollama_base}/api/tags", optional=True)

    print("Smoke test completed.")


if __name__ == "__main__":
    main()
