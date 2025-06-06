# Send a message to the MCP server
param(
    [Parameter(Mandatory=$true)]
    [string]$Content,
    
    [Parameter()]
    [string]$Type = "prompt",
    
    [Parameter()]
    [hashtable]$Metadata = @{}
)

$messageObj = @{
    type = $Type
    content = $Content
    metadata = $Metadata
}

$messageJson = $messageObj | ConvertTo-Json -Depth 10 -Compress
Write-Host "Sending message: $messageJson" -ForegroundColor Gray

# Send the message to the container
$result = "$messageJson`n" | docker exec -i mcp-server-demo python -u main.py *>&1

# Process and display the results
$result | ForEach-Object {
    if ($_ -match "^\{.*\}$") {
        try {
            $response = $_ | ConvertFrom-Json
            Write-Host "`nServer response:" -ForegroundColor Green
            Write-Host "Type: $($response.type)" -ForegroundColor Cyan
            Write-Host "Content: $($response.content)" -ForegroundColor Cyan
            if ($response.metadata.PSObject.Properties.Count -gt 0) {
                Write-Host "Metadata:" -ForegroundColor Cyan
                $response.metadata | Format-Table
            }
        } catch {
            Write-Host "Failed to parse response: $_" -ForegroundColor Red
        }
    }
    elseif ($_ -match "^\d{4}-\d{2}-\d{2}") {
        Write-Host $_ -ForegroundColor DarkGray
    }
}
