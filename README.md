# Guardian Firewall

Real-time grooming risk firewall for game chats

## Overview

Guardian monitors live game chats, detects grooming risk at the conversation level, and intervenes with safety pauses, inline highlights, and a guardian alert feed.

## Architecture

```
guardian_firewall/
├── frontend/          # React + Vite landing page
│   ├── src/
│   │   ├── App.tsx    # Main landing page
│   │   └── App.css    # Cybersecurity-themed styling
│   └── package.json
└── README.md
```

## Quick Start

```bash
# Install and run frontend
cd frontend
npm install
npm run dev
```

## Features

- 🔍 **Multi-turn Detection**: ML + precision rules track risk escalation
- ⏸️ **Safety Pause**: Intercepts risky messages with safe alternatives  
- 📊 **Guardian Portal**: Real-time incident dashboard with platform reporting

## Tech Stack

- **Frontend**: React + TypeScript + Vite
- **Styling**: Modern CSS with cybersecurity theme
- **Design**: Cloudflare-inspired dark UI