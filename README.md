# MCP Server Demo (Humorous Edition)

A simplified Model Context Protocol (MCP) server implemented in Python. This version reads plain text from standard input and responds with a humorous message. It is Docker- and Azure-deployable.

## Project Structure



```
.
├── infrastructure/           # Infrastructure and deployment related files
│   ├── azure/              # Azure deployment files
│   │   ├── deploy.ps1     # PowerShell deployment script
│   │   ├── deploy.sh      # Bash deployment script
│   │   └── main.bicep     # Azure Bicep deployment template
│   └── docker/            # Docker deployment files
│       ├── Dockerfile     # Container definition
│       └── docker-compose.yml # Docker Compose configuration
├── main.py                 main.py # MCP server implementation (reads text, returns funny responses)
└── requirements.txt        # Python dependencies
```

## Development

To run the MCP server locally:

```powershell
python main.py
```

To run with Docker:
```powershell
cd infrastructure/docker
docker compose up --build   # Build and start the container
docker compose down        # Stop and remove the container
```

To test the MCP server, send a message:
```powershell
echo '{"type": "prompt", "content": "Hello MCP Server!", "metadata": {}}' | docker compose exec -T mcp-server-demo python -u main.py
```

## Deployment

To deploy to Azure:

```powershell
cd infrastructure/azure
./deploy.ps1
```

Make sure you have the Azure CLI installed and are logged in before deploying.
