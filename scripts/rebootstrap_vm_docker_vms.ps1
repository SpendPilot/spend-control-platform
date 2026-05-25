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
    "module.frontend_vmss.azurerm_linux_virtual_machine_scale_set.this",
    "module.backend_vmss.azurerm_linux_virtual_machine_scale_set.this",
    "module.data_ai_vmss.azurerm_linux_virtual_machine_scale_set.this"
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
