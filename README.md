# Guardian Firewall

Real-time grooming risk firewall for game chats

## Overview

Guardian monitors live game chats, detects grooming risk at the conversation level, and intervenes with safety pauses, inline highlights, and a guardian alert feed.

## Architecture

```
guardian_firewall/
├── backend/
│   ├── app.py                 # FastAPI server with WebSocket, health endpoints, CORS
│   ├── requirements.txt       # Dependencies (FastAPI, uvicorn, websockets)
│   ├── routes/
│   │   └── classify.py        # Risk analysis API - /api/classify/message endpoint
│   └── risk/
│       ├── rules.py           # Grooming patterns - Age probing, secrecy, meeting requests
│       ├── model.py           # ML wrapper - Placeholder for transformer model
│       └── fuse.py            # Score fusion - Combines ML + rules → final risk level
├── frontend/                  # React + Vite (ready for integration)
├── models/
│   └── config.yaml           # Thresholds & weights configuration
└── .gitignore                # Excludes venv, __pycache__, node_modules, .env, etc.
```

## Quick Start

### Backend
```bash
# Activate virtual environment and start backend
cd backend
source ../myvenv/bin/activate
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
# Install and run frontend
cd frontend
npm install
npm run dev
```

## File Overview

### 🔥 Core Backend (4 files)
- `backend/app.py` - **FastAPI server** with WebSocket, health endpoints, CORS
- `backend/requirements.txt` - **Dependencies** (FastAPI, uvicorn, websockets)
- `backend/routes/classify.py` - **Risk analysis API** - `/api/classify/message` endpoint

### 🧠 Risk Engine (3 files)
- `backend/risk/rules.py` - **Grooming patterns** - Age probing, secrecy, meeting requests
- `backend/risk/model.py` - **ML wrapper** - Placeholder for transformer model
- `backend/risk/fuse.py` - **Score fusion** - Combines ML + rules → final risk level

### ⚙️ Config
- `models/config.yaml` - **Thresholds & weights**

### 🎨 Frontend
- `frontend/` - **React + Vite** (ready for integration)

## What Each Core File Does

1. **`app.py`** - Starts server, handles WebSocket connections, processes chat messages
2. **`rules.py`** - Detects grooming patterns: "how old are you?", "keep this secret", "meet up"
3. **`fuse.py`** - Combines rule + ML scores → LOW/MEDIUM/HIGH risk + safety suggestions
4. **`classify.py`** - REST API for frontend to send messages and get risk assessment

## API Endpoints

- `GET /health` - Health check
- `GET /` - API status
- `POST /api/classify/message` - Classify single message for risk
- `POST /api/classify/conversation` - Analyze conversation patterns
- `WS /ws` - WebSocket for real-time updates

## Features

- 🔍 **Multi-turn Detection**: ML + precision rules track risk escalation
- ⏸️ **Safety Pause**: Intercepts risky messages with safe alternatives
- 📊 **Guardian Portal**: Real-time incident dashboard with platform reporting

## Tech Stack

- **Backend**: FastAPI + Python
- **Frontend**: React + TypeScript + Vite
- **Real-time**: WebSockets
- **AI**: Transformer models + rule-based detection