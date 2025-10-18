#!/usr/bin/env bash
set -e

# === CONFIG ===
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$BASE_DIR/logs"
mkdir -p "$LOG_DIR"

# Helper function to wait for a port
wait_for_port() {
    local port=$1
    local name=$2
    echo "Waiting for $name to start on port $port..."
    while ! nc -z localhost "$port" >/dev/null 2>&1; do
        sleep 1
    done
    echo "$name is up!"
}

# === 1. Ollama Serve ===
echo "Starting Ollama..."
nohup ollama serve > "$LOG_DIR/ollama.log" 2>&1 &
wait_for_port 11434 "Ollama"

# === 2. Whisper Server ===
echo "Starting Whisper Server..."
cd ./openvino/whisper || exit
nohup uv run app.py > "$LOG_DIR/whisper.log" 2>&1 &
wait_for_port 4896 "Whisper Server"

# === 3. ADK Server ===
echo "Starting ADK Server..."
cd ../../agent || exit
nohup uv run adk web > "$LOG_DIR/adk.log" 2>&1 &
wait_for_port 8000 "ADK Server"

# === 4. MCP Server ===
echo "Starting MCP Server..."
cd ./mcp || exit
nohup uv run server.py > "$LOG_DIR/mcp.log" 2>&1 &
wait_for_port 6969 "MCP Server"

# === 5. gRPC Server ===
echo "Starting gRPC Server..."
cd ../../backend || exit
nohup uv run grpc_server.py > "$LOG_DIR/grpc.log" 2>&1 &
wait_for_port 50051 "gRPC Server"

# === 6. gRPC Gateway ===
echo "Starting gRPC Gateway..."
nohup uv run gateway.py > "$LOG_DIR/gateway.log" 2>&1 &
wait_for_port 1234 "gRPC Gateway"

# === 7. Frontend ===
echo "Starting Frontend..."
cd ../frontend || exit
nohup npm run tauri dev > "$LOG_DIR/frontend.log" 2>&1 &
wait_for_port 5173 "Frontend"

echo "All services are running successfully!"
