# Spend Control Platform Runbook

## Required sibling repos

- `../spend-control-frontend`
- `../spend-control-control-service`
- `../spend-control-expense-service`
- `../spend-control-ai-service`

## Bring up the full stack

```powershell
cd c:\Users\lijaz\Desktop\PROJECT2\spend-control-platform
docker compose up --build
```

## Health endpoints

- frontend: `http://localhost:3000`
- control-service: `http://localhost:8000/health`
- expense-service: `http://localhost:8001/health`
- ai-service: `http://localhost:8002/health`
- ollama: `http://localhost:11434/api/tags`

## Common failures

### Docker daemon not running

Start Docker Desktop, then retry:

```powershell
docker version
```

### One repo is missing

Compose builds from sibling repos. If one folder is missing, recreate or clone it beside `spend-control-platform`.

### Ollama unavailable

AI falls back safely, but to restore model responses:

```powershell
ollama serve
ollama pull llama3.1:8b
```

### Verify the split setup

```powershell
py -3.13 scripts/smoke_test.py
```

