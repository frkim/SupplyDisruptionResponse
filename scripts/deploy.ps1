# Builds the container image in ACR and deploys/updates the Container App.
# Usage:  pwsh ./scripts/deploy.ps1

$ErrorActionPreference = 'Stop'

$ResourceGroup = 'rg-supply-disruption'
$CoreDeployment = 'sdr-core'
$Root = Split-Path -Parent $PSScriptRoot

Write-Host '==> Reading core deployment outputs' -ForegroundColor Cyan
$outputs = az deployment group show `
    --resource-group $ResourceGroup `
    --name $CoreDeployment `
    --query properties.outputs -o json | ConvertFrom-Json

$acrName = $outputs.acrName.value
$acrLoginServer = $outputs.acrLoginServer.value
$tag = "v$(Get-Date -Format 'yyyyMMddHHmmss')"
$image = "$acrLoginServer/supply-disruption:$tag"

Write-Host "==> Building image $image" -ForegroundColor Cyan
az acr build `
    --registry $acrName `
    --image "supply-disruption:$tag" `
    --file "$Root/Dockerfile" `
    $Root
if ($LASTEXITCODE -ne 0) { throw 'Image build failed.' }

Write-Host '==> Deploying container app' -ForegroundColor Cyan
az deployment group create `
    --resource-group $ResourceGroup `
    --name "sdr-app-$tag" `
    --template-file "$Root/infra/app.bicep" `
    --parameters `
        containerAppEnvironmentId=$($outputs.containerAppEnvironmentId.value) `
        acrLoginServer=$acrLoginServer `
        containerImage=$image `
        identityId=$($outputs.identityId.value) `
        identityClientId=$($outputs.identityClientId.value) `
        aiProjectEndpoint=$($outputs.aiProjectEndpoint.value) `
        openAiEndpoint=$($outputs.openAiEndpoint.value) `
        modelDeploymentName=$($outputs.modelDeploymentName.value) `
        embeddingDeploymentName=$($outputs.embeddingDeploymentName.value) `
        cosmosEndpoint=$($outputs.cosmosEndpoint.value) `
        searchEndpoint=$($outputs.searchEndpoint.value) `
        storageBlobEndpoint=$($outputs.storageBlobEndpoint.value) `
        appInsightsConnectionString=$($outputs.appInsightsConnectionString.value) `
    --query properties.outputs -o json | Tee-Object -Variable appOut
if ($LASTEXITCODE -ne 0) { throw 'Container app deployment failed.' }

$appUrl = ($appOut | ConvertFrom-Json).appUrl.value
Write-Host ''
Write-Host "Deployed: $appUrl" -ForegroundColor Green
Write-Host "Image tag: $tag" -ForegroundColor Green
