# Guardian Firewall

Guardian Firewall is a comprehensive, real-time grooming risk firewall for live game chats. It monitors gaming conversations, detects grooming and predatory risks at the conversation level, and intervenes with safety pauses, inline highlights, and a guardian alert feed—all powered by a fusion of AI models and rule-based analysis.

---

## Table of Contents

- [Key Features](#key-features)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Core Components](#core-components)
- [API Endpoints](#api-endpoints)
- [Tech Stack](#tech-stack)
- [Future Roadmap](#future-roadmap)
- [License](#license)

---

## Key Features

- **Real-Time Multi-Turn Detection:** Combines transformer-based AI and precise rules to track risk escalation over conversations.
- **Safety Pausing:** Intercepts risky messages and suggests safer alternatives.
- **Guardian Portal:** Incident dashboard for real-time alerts and reporting.
- **Inline Risk Highlighting:** Flags dangerous content directly in chat.
- **Customizable Risk Thresholds:** Configure detection sensitivity via YAML.
- **WebSocket-Powered Live Updates:** Instant risk feedback for users and moderators.

---

## Architecture Overview

```
guardian_firewall/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── routes/
│   │   └── classify.py
│   └── risk/
│       ├── rules.py
│       ├── model.py
│       └── fuse.py
├── frontend_new/                 # React + Vite (ready for integration)
├── models/
│   └── config.yaml
├── chat-server.js
├── PRESENTATION_SLIDES.md
├── test_detector.py
├── .gitignore
└── README.md
```

---

## Project Structure

- **backend/** — FastAPI server, WebSocket support, ML and rules-based risk detection.
  - `app.py` — FastAPI app entrypoint, WebSocket routing, health checks.
  - `requirements.txt` — Python dependencies.
  - `routes/classify.py` — REST endpoints for message/conversation classification.
  - `risk/rules.py` — Detects grooming patterns (e.g., age probing, secrecy).
  - `risk/model.py` — ML model wrapper (plug in transformer or other models).
  - `risk/fuse.py` — Score fusion (combines rules and ML for final risk assessment).
- **frontend_new/** — Modern React (Vite) frontend for moderator and user interfaces.
- **models/config.yaml** — Configurable risk thresholds, weights, and model settings.
- **chat-server.js** — (Optional/legacy) Standalone chat server for testing.
- **test_detector.py** — Python test suite for risk detection logic.
- **PRESENTATION_SLIDES.md** — Project slides/documentation.

---

## Getting Started

### Backend

1. **Create a Python virtual environment** (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install dependencies:**

    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3. **Run the backend server:**

    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```

### Frontend

1. **Navigate to the frontend directory:**

    ```bash
    cd frontend_new
    ```

2. **Install dependencies:**

    ```bash
    npm install
    ```

3. **Run the development server:**

    ```bash
    npm run dev
    ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Core Components

### Backend

- **`app.py`** — Main FastAPI application, sets up API and WebSocket routes.
- **`routes/classify.py`** — `/api/classify/message` and `/api/classify/conversation` endpoints for risk analysis.
- **`risk/rules.py`** — Implements common grooming detection patterns (e.g., "how old are you?", "keep this secret", "let's meet").
- **`risk/model.py`** — Integrate ML models for nuanced language detection.
- **`risk/fuse.py`** — Fuses rule-based and ML outputs into a single risk score.

### Frontend

- **React + Vite** — Responsive dashboard for real-time alerts, chat monitoring, and moderation tools.

### Models

- **`models/config.yaml`** — Adjust risk levels, thresholds, and weights for different detection modules.

---

## API Endpoints

- `GET /health` — Server health check.
- `GET /` — API status.
- `POST /api/classify/message` — Classifies a single chat message for grooming/predatory risk.
- `POST /api/classify/conversation` — Analyzes an entire conversation for escalation patterns.
- `WS /ws` — Real-time WebSocket stream for live chat monitoring and feedback.

---

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, WebSockets
- **Frontend:** React, TypeScript, Vite
- **ML/AI:** Transformer models (pluggable), rule-based NLP
- **Config:** YAML for risk and model tuning

---

## Future Roadmap

- **Full Dashboard:** Moderator tools, report center, analytics.
- **Expanded AI:** Integrate more advanced language models.
- **Custom Rules:** User-defined or organization-specific risk patterns.
- **Notification Center:** Real-time alerts for parents/guardians.
- **Plugin Support:** Extend detection for other chat/game platforms.

---

## License

Private project for Guardian Firewall development.

---
