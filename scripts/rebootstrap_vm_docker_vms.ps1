param(
    [string]$TerraformDir = (Join-Path $PSScriptRoot "..\terraform\azure\vm-docker"),
    [string]$TfvarsFile = "terraform.tfvars",
    [switch]$PlanOnly
)

$ErrorActionPreference = "Stop"

$terraformPath = (Resolve-Path $TerraformDir).Path
$tfvarsPath = Join-Path $terraformPath $TfvarsFile

if (-not (Test-Path $tfvarsPath)) {
    throw "Terraform variables file not found: $tfvarsPath"
}

$replaceTargets = @(
    "module.frontend_vms.azurerm_linux_virtual_machine.this[0]",
    "module.backend_vms.azurerm_linux_virtual_machine.this[0]",
    "module.data_vms.azurerm_linux_virtual_machine.this[0]"
)

$replaceArgs = @()
foreach ($target in $replaceTargets) {
    $replaceArgs += "-replace=$target"
}

Push-Location $terraformPath
try {
    terraform init -upgrade

    if ($PlanOnly) {
        terraform plan -var-file $TfvarsFile @replaceArgs
    }
    else {
        terraform apply -var-file $TfvarsFile @replaceArgs
    }
}
finally {
    Pop-Location
}
