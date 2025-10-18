# GenAI Desktop Application

A **fully local AI desktop application** capable of analyzing and querying **short video files**. The application can **extract and summarize content**, **generate reports (PDF/PPT)**, and  **operate entirely offline** using **local AI models** and **MCP servers**.

---

## Prerequisites

- **Operating System:** Ubuntu 22.04 or 24.10  
- **Hardware:** Intel Platform (Meteor Lake and above)  
- **Package Manager:** [uv](https://github.com/astral-sh/uv) — Python package & virtual environment manager  

Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/genai-desktop.git
cd genai-desktop
```

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run tauri dev
```

### 3. Setup Backend
```bash
cd backend
uv venv
uv pip install -r requirements.txt
```

### 4. Setup Agent
```bash
cd agent
uv venv
uv pip install -r requirements.txt
```

### 5. Setup Whisper (OpenVINO)
```bash
cd openvino/whisper
uv venv
uv pip install -r requirements.txt
```

### 6. Run the Whole Application

Make sure your run.sh file is executable:
```bash
chmod +x run.sh
```

Then start everything:
```bash
./run.sh
```

## 🧩 Features

- 🎥 **Video Analysis** – Extract key frames and insights from short clips  
- 🧾 **Summarization & Querying** – Ask natural language questions about videos  
- 📑 **Report Generation** – Export PDF and PowerPoint summaries  
- 🔒 **Offline-First Design** – 100% local inference using OpenVINO and MCP  
- 🖥️ **Cross-Component Orchestration** – Seamless backend–agent–whisper integration

📁 Project Structure
```
genai-desktop/
├── frontend/          # Tauri + React desktop frontend
├── backend/           # FastAPI and gRPC backend
├── agent/             # AI agent service
├── openvino/whisper/  # Openvino speech to text service
└── run.sh             # Script to launch all services
```

## 🧠 Technology Stack

- **Frontend:** Tauri + React  
- **Backend:** FastAPI + gRPC  
- **AI Models:** OpenVINO, Whisper  
- **Environment:** uv (Python), Node.js  
- **Platform:** Intel GPU acceleration (Meteor Lake and above)
