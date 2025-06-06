# Test different message types for the MCP server
param(
    [Parameter(Position=0)]
    [string]$Message = "Hello from MCP test script!",
    
    [Parameter()]
    [switch]$ShowLogs,
    
    [Parameter()]
    [switch]$FollowLogs
)

# Ensure we're in the docker directory
Set-Location -Path $PSScriptRoot

# Make sure the container is running
docker compose up -d

# Create the test message
$testMessage = @{
    type = "prompt"
    content = $Message
    metadata = @{
    }
} | ConvertTo-Json

Write-Host "`nSending test message..." -ForegroundColor Cyan
$testMessage | docker exec -i mcp-server-demo python -u main.py

if ($ShowLogs) {
    Write-Host "`nServer logs:" -ForegroundColor Yellow
    docker logs mcp-server-demo
}

if ($FollowLogs) {
    Write-Host "`nFollowing server logs (Ctrl+C to stop):" -ForegroundColor Yellow
    docker logs -f mcp-server-demo
}

Write-Host "`nAvailable commands:" -ForegroundColor Green
Write-Host "1. View logs: docker logs mcp-server-demo" -ForegroundColor Yellow
Write-Host "2. Follow logs: docker logs -f mcp-server-demo" -ForegroundColor Yellow
Write-Host "3. Stop server: docker compose down" -ForegroundColor Yellow
