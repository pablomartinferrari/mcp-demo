#!/bin/bash

# Variables
RESOURCE_GROUP="mcp-server-rg"
LOCATION="eastus"  # Change this to your preferred location
ACR_NAME="mcpserverregistry"  # Must be globally unique
CONTAINER_NAME="mcp-server-container"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# Build and push the container
az acr build --registry $ACR_NAME --image mcp-server:latest .

# Deploy using the ARM template
az deployment group create \
    --resource-group $RESOURCE_GROUP \
    --template-file azuredeploy.json \
    --parameters \
        containerRegistryName=$ACR_NAME \
        containerInstanceName=$CONTAINER_NAME
