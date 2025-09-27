from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import json
from datetime import datetime
from routes.classify import router as classify_router
from risk.fuse import RiskFusion

# Simple lifespan without database for now
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Guardian Firewall",
    description="Real-time grooming risk detection for game chats",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(classify_router, prefix="/api")

# WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass

manager = ConnectionManager()
risk_fusion = RiskFusion()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Process message through risk engine
            risk_result = risk_fusion.analyze_message(
                message_data.get("text", ""),
                message_data.get("conversation_history", [])
            )

            # Broadcast risk update
            await manager.broadcast({
                "type": "risk_update",
                "level": risk_result["level"],
                "score": risk_result["score"],
                "explanations": risk_result["explanations"]
            })

            # If high risk, trigger safety pause
            if risk_result["level"] == "high":
                await manager.broadcast({
                    "type": "safety_pause",
                    "message": "This message may contain inappropriate content. Please review before sending.",
                    "suggestions": risk_result.get("suggestions", [])
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "Guardian Firewall API", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)