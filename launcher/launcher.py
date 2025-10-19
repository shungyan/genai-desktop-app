import os
import subprocess
import socket
import time


# === CONFIG ===
# Current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go one level up
BASE_DIR = os.path.dirname(current_dir)
LOG_DIR = os.path.join(BASE_DIR, "logs/windows")
os.makedirs(LOG_DIR, exist_ok=True)


def wait_for_port(port, name):
    """Wait until a given port on localhost is open."""
    print(f"Waiting for {name} to start on port {port}...")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", port))
            if result == 0:
                print(f"{name} is up!")
                break
        time.sleep(1)


def run_background(command, cwd, log_file):
    """Run a command in the background and log its output."""
    with open(log_file, "a") as log:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=log,
            stderr=subprocess.STDOUT,
            bufsize=1,
        )
    return process


def main():

    # === 2. Whisper Server ===
    print("Starting Whisper Server...")
    whisper_dir = os.path.join(BASE_DIR, "openvino", "whisper")
    run_background("uv run app.py", whisper_dir, os.path.join(LOG_DIR, "whisper.log"))
    wait_for_port(4896, "Whisper Server")

    # === 3. ADK Server ===
    print("Starting ADK Server...")
    adk_dir = os.path.join(BASE_DIR, "agent")
    run_background("uv run adk web", adk_dir, os.path.join(LOG_DIR, "adk.log"))
    wait_for_port(8000, "ADK Server")

    # === 4. MCP Server ===
    print("Starting MCP Server...")
    mcp_dir = os.path.join(adk_dir, "mcp")
    run_background("uv run server.py", mcp_dir, os.path.join(LOG_DIR, "mcp.log"))
    wait_for_port(6969, "MCP Server")

    # === 5. gRPC Server ===
    print("Starting gRPC Server...")
    backend_dir = os.path.join(BASE_DIR, "backend")
    run_background("uv run grpc_server.py", backend_dir, os.path.join(LOG_DIR, "grpc.log"))
    wait_for_port(50051, "gRPC Server")

    # === 6. gRPC Gateway ===
    print("Starting gRPC Gateway...")
    run_background("uv run gateway.py", backend_dir, os.path.join(LOG_DIR, "gateway.log"))
    wait_for_port(1234, "gRPC Gateway")

    # === 7. Frontend ===
    print("Starting Frontend...")
    frontend_dir = os.path.join(BASE_DIR, "frontend")
    run_background("npm run tauri dev", frontend_dir, os.path.join(LOG_DIR, "frontend.log"))
    wait_for_port(5173, "Frontend")

    print("All services are running successfully!")


if __name__ == "__main__":
    main()
