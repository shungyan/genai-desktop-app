#!/usr/bin/env pwsh
# Exit on error
$ErrorActionPreference = "Stop"

# === CONFIG ===
$BASE_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$LOG_DIR = Join-Path $BASE_DIR "logs"
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null

# Helper function to wait for a port
function Wait-ForPort {
    param(
        [int]$Port,
        [string]$Name
    )

    Write-Host "Waiting for $Name to start on port $Port..."
    while (-not (Test-NetConnection -ComputerName "localhost" -Port $Port -InformationLevel Quiet)) {
        Start-Sleep -Seconds 1
    }
    Write-Host "$Name is up!"
}


# === 2. Whisper Server ===
Write-Host "Starting Whisper Server..."
Set-Location "$BASE_DIR\openvino\whisper"
Start-Process -FilePath "uv" -ArgumentList "run app.py" -RedirectStandardOutput "$LOG_DIR\whisper.log" -RedirectStandardError "$LOG_DIR\whisper.log" -WindowStyle Hidden
Wait-ForPort 4896 "Whisper Server"

# === 3. ADK Server ===
Write-Host "Starting ADK Server..."
Set-Location "$BASE_DIR\agent"
Start-Process -FilePath "uv" -ArgumentList "run adk web" -RedirectStandardOutput "$LOG_DIR\adk.log" -RedirectStandardError "$LOG_DIR\adk.log" -WindowStyle Hidden
Wait-ForPort 8000 "ADK Server"

# === 4. MCP Server ===
Write-Host "Starting MCP Server..."
Set-Location "$BASE_DIR\agent\mcp"
Start-Process -FilePath "uv" -ArgumentList "run server.py" -RedirectStandardOutput "$LOG_DIR\mcp.log" -RedirectStandardError "$LOG_DIR\mcp.log" -WindowStyle Hidden
Wait-ForPort 6969 "MCP Server"

# === 5. gRPC Server ===
Write-Host "Starting gRPC Server..."
Set-Location "$BASE_DIR\backend"
Start-Process -FilePath "uv" -ArgumentList "run grpc_server.py" -RedirectStandardOutput "$LOG_DIR\grpc.log" -RedirectStandardError "$LOG_DIR\grpc.log" -WindowStyle Hidden
Wait-ForPort 50051 "gRPC Server"

# === 6. gRPC Gateway ===
Write-Host "Starting gRPC Gateway..."
Start-Process -FilePath "uv" -ArgumentList "run gateway.py" -RedirectStandardOutput "$LOG_DIR\gateway.log" -RedirectStandardError "$LOG_DIR\gateway.log" -WindowStyle Hidden
Wait-ForPort 1234 "gRPC Gateway"

# === 7. Frontend ===
Write-Host "Starting Frontend..."
Set-Location "$BASE_DIR\frontend"
Start-Process -FilePath "npm" -ArgumentList "run tauri dev" -RedirectStandardOutput "$LOG_DIR\frontend.log" -RedirectStandardError "$LOG_DIR\frontend.log" -WindowStyle Hidden
Wait-ForPort 5173 "Frontend"

Write-Host "`n All services are running successfully!"
