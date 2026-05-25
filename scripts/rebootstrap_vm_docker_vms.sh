#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TERRAFORM_DIR="${1:-$SCRIPT_DIR/../terraform/azure/vm-docker}"
TFVARS_FILE="${TFVARS_FILE:-terraform.tfvars}"
MODE="${MODE:-apply}"

cd "$TERRAFORM_DIR"

if [[ ! -f "$TFVARS_FILE" ]]; then
  echo "Terraform variables file not found: $TERRAFORM_DIR/$TFVARS_FILE" >&2
  exit 1
fi

REPLACE_ARGS=(
  "-replace=module.frontend_vmss.azurerm_linux_virtual_machine_scale_set.this"
  "-replace=module.backend_vmss.azurerm_linux_virtual_machine_scale_set.this"
  "-replace=module.data_ai_vmss.azurerm_linux_virtual_machine_scale_set.this"
)

terraform init -upgrade

if [[ "$MODE" == "plan" ]]; then
  terraform plan -var-file="$TFVARS_FILE" "${REPLACE_ARGS[@]}"
else
  terraform apply -var-file="$TFVARS_FILE" "${REPLACE_ARGS[@]}"
fi
