# Spend Control Platform - Clone All Repositories Script
# This script clones all required repositories for the Spend Control platform
# 
# Run from spend-control-platform directory:
#   .\clone-all-repos.ps1
#
# This will clone all repos into the same directory as spend-control-platform

param(
    [Parameter(HelpMessage="Base directory to clone repositories into (defaults to parent directory)")]
    [string]$BaseDir = $(Split-Path -Parent (Split-Path -Parent $PSCommandPath))
)

# Define repository information
$repositories = @(
    @{
        Name = "spend-control-platform"
        Url  = "https://github.com/your-org/spend-control-platform.git"
    },
    @{
        Name = "spend-control-ai-service"
        Url  = "https://github.com/your-org/spend-control-ai-service.git"
    },
    @{
        Name = "spend-control-control-service"
        Url  = "https://github.com/your-org/spend-control-control-service.git"
    },
    @{
        Name = "spend-control-expense-service"
        Url  = "https://github.com/your-org/spend-control-expense-service.git"
    },
    @{
        Name = "spend-control-frontend"
        Url  = "https://github.com/your-org/spend-control-frontend.git"
    }
)

# Create base directory if it doesn't exist
if (-not (Test-Path $BaseDir)) {
    Write-Host "Creating base directory: $BaseDir" -ForegroundColor Green
    New-Item -ItemType Directory -Path $BaseDir -Force | Out-Null
}

Set-Location $BaseDir
Write-Host "Working in directory: $(Get-Location)" -ForegroundColor Cyan

# Clone each repository
foreach ($repo in $repositories) {
    $repoPath = Join-Path $BaseDir $repo.Name
    
    if (Test-Path $repoPath) {
        Write-Host "Repository already exists: $($repo.Name)" -ForegroundColor Yellow
        Set-Location $repoPath
        Write-Host "Pulling latest changes for $($repo.Name)..." -ForegroundColor Cyan
        git pull
        Set-Location $BaseDir
    }
    else {
        Write-Host "Cloning $($repo.Name)..." -ForegroundColor Green
        git clone $repo.Url $repo.Name
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Successfully cloned: $($repo.Name)" -ForegroundColor Green
        }
        else {
            Write-Host "Failed to clone: $($repo.Name)" -ForegroundColor Red
        }
    }
}

Write-Host "`nRepository setup complete!" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Copy .env.example to .env in spend-control-platform:"
Write-Host "   Copy-Item spend-control-platform/.env.example spend-control-platform/.env"
Write-Host ""
Write-Host "2. Start infrastructure services (PostgreSQL, Ollama):"
Write-Host "   cd spend-control-platform"
Write-Host "   docker compose -f docker-compose.infrastructure.yml up --build"
Write-Host ""
Write-Host "3. In a new terminal, start backend services:"
Write-Host "   cd spend-control-platform"
Write-Host "   docker compose -f docker-compose.backend.yml up --build"
Write-Host ""
Write-Host "4. In another terminal, start frontend:"
Write-Host "   cd spend-control-platform"
Write-Host "   docker compose -f docker-compose.frontend.yml up --build"
