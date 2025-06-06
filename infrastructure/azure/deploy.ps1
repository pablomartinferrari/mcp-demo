# Azure deployment variables
$RESOURCE_GROUP = "mcp-server-demo-rg"
$LOCATION = "eastus"  # Change this to your preferred location
$ACR_NAME = "mcpserverdemoreg"  # Must be globally unique
$CONTAINER_NAME = "mcp-server-demo-container"

# Store the root directory path
$ROOT_DIR = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled $true

# Build and push the container (from the root directory where Dockerfile is)
Set-Location $ROOT_DIR
az acr build --registry $ACR_NAME --image mcp-server:latest --file infrastructure/docker/Dockerfile .

# Deploy using the Bicep template
az deployment group create `
    --resource-group $RESOURCE_GROUP `
    --template-file $PSScriptRoot/main.bicep `
    --parameters containerRegistryName=$ACR_NAME containerInstanceName=$CONTAINER_NAME

# Return to the original directory
Set-Location $PSScriptRoot

Write-Host "`nCost Management Commands:" -ForegroundColor Yellow
Write-Host "To stop the container (pause costs):" -ForegroundColor Green
Write-Host "az container stop --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP"
Write-Host "`nTo start the container again:" -ForegroundColor Green
Write-Host "az container start --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP"
Write-Host "`nTo delete all resources (stop all costs):" -ForegroundColor Green
Write-Host "az group delete --name $RESOURCE_GROUP --yes"
Write-Host "`nEstimated daily cost:" -ForegroundColor Yellow
Write-Host "ACR Basic: ~$0.167/day" -ForegroundColor Cyan
Write-Host "Container Instance (if running 24/7): ~$1.25/day" -ForegroundColor Cyan