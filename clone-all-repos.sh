#!/bin/bash

# Spend Control Platform - Clone All Repositories Script
# This script clones all required repositories for the Spend Control platform
#
# Run from spend-control-platform directory:
#   ./clone-all-repos.sh
#
# This will clone all repos into the same directory as spend-control-platform

# Get the directory where this script is located (platform directory)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Default to parent directory (where platform repo is)
BASE_DIR="${1:-.}"
if [ "$BASE_DIR" = "." ]; then
    BASE_DIR="$(dirname "$SCRIPT_DIR")"
fi

# Define repository information
declare -a REPOSITORIES=(
    "spend-control-platform:https://github.com/SpendPilot/spend-control-platform.git"
    "spend-control-ai-service:https://github.com/SpendPilot/spend-control-ai-service.git"
    "spend-control-control-service:https://github.com/SpendPilot/spend-control-control-service.git"
    "spend-control-expense-service:https://github.com/SpendPilot/spend-control-expense-service.git"
    "spend-control-frontend:https://github.com/SpendPilot/spend-control-frontend.git"
)

# Create base directory if it doesn't exist
if [ ! -d "$BASE_DIR" ]; then
    echo -e "\033[32mCreating base directory: $BASE_DIR\033[0m"
    mkdir -p "$BASE_DIR"
fi

cd "$BASE_DIR"
echo -e "\033[36mWorking in directory: $(pwd)\033[0m"

# Clone each repository
for repo_info in "${REPOSITORIES[@]}"; do
    IFS=':' read -r repo_name repo_url <<< "$repo_info"
    
    if [ -d "$repo_name" ]; then
        echo -e "\033[33mRepository already exists: $repo_name\033[0m"
        cd "$repo_name"
        echo -e "\033[36mPulling latest changes for $repo_name...\033[0m"
        git pull
        cd ..
    else
        echo -e "\033[32mCloning $repo_name...\033[0m"
        git clone "$repo_url" "$repo_name"
        if [ $? -eq 0 ]; then
            echo -e "\033[32mSuccessfully cloned: $repo_name\033[0m"
        else
            echo -e "\033[31mFailed to clone: $repo_name\033[0m"
        fi
    fi
done

echo -e "\n\033[36mRepository setup complete!\033[0m"
echo -e "\033[32mNext steps:\033[0m"
echo "1. Copy .env.example to .env in spend-control-platform:"
echo "   cp spend-control-platform/.env.example spend-control-platform/.env"
echo ""
echo "2. Start infrastructure services (PostgreSQL, Ollama):"
echo "   cd spend-control-platform"
echo "   docker compose -f docker-compose.infrastructure.yml up --build"
echo ""
echo "3. In a new terminal, start backend services:"
echo "   cd spend-control-platform"
echo "   docker compose -f docker-compose.backend.yml up --build"
echo ""
echo "4. In another terminal, start frontend:"
echo "   cd spend-control-platform"
echo "   docker compose -f docker-compose.frontend.yml up --build"
