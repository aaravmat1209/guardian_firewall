<<<<<<< HEAD
# Guardian AI

A React-based child safety monitoring system for gaming chats, featuring advanced AI-powered threat detection and real-time content filtering.

## Design System

This application follows the design patterns inspired by [Quantra Security](https://quantra-security.webflow.io/) with our custom Guardian AI color scheme and branding.

### Key Features

- **Quantra-Inspired Design**: Modern, professional aesthetic with smooth animations
- **Custom Color Scheme**: Red accent colors (#DC2626) on dark backgrounds
- **Space Grotesk Typography**: Clean, geometric font matching Quantra's style
- **Responsive Design**: Mobile-first approach with smooth transitions
- **Advanced Animations**: Fade-in effects, hover states, and scroll-triggered animations

### Color Palette

```css
--color-black: #000000;
--color-dark: #0a0a0a;
--color-red: #DC2626;
--color-red-bright: #FF0000;
--color-white: #FFFFFF;
--color-gray: #E5E5E5;
--color-red-glow: rgba(220, 38, 38, 0.5);
--color-red-dim: rgba(220, 38, 38, 0.2);
```

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Removes the single build dependency

## Project Structure

```
src/
├── components/
│   ├── Navbar.jsx
│   └── Hero.jsx
├── styles/
│   ├── globals.css
│   ├── Navbar.css
│   └── Hero.css
├── App.jsx
└── index.js
```

## Components

### Navbar
- Fixed navigation with blur background
- Guardian AI branding with red accent
- Smooth hover animations
- Mobile-responsive hamburger menu

### Hero
- Full viewport height with animated content
- Quantra-style fade-up animations
- Interactive mouse-tracking glow effect
- Statistics display and call-to-action buttons

## Design Implementation

The design closely follows Quantra's aesthetic while maintaining Guardian AI's unique identity:

- **Typography**: Space Grotesk font with uppercase headings and proper letter spacing
- **Animations**: Smooth fade-in effects with staggered timing
- **Layout**: Clean grid system with consistent spacing
- **Interactive Elements**: Hover effects with glow and transform animations
- **Color Usage**: Strategic use of red accents on dark backgrounds

## Future Development

This is the foundation for a comprehensive child safety monitoring platform. Future features will include:

- Real-time chat monitoring dashboard
- AI threat detection analytics
- Content filtering controls
- Safety reporting system
- Parent/guardian notification center

## License

Private project for Guardian AI development.
=======
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
>>>>>>> 012c98023ebff729f24c82772ca0731c415c9a94
