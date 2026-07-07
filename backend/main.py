"""
ASTRAIOS Backend — Application entrypoint

Run with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers.health import router as health_router
from routers.mission import router as mission_router

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for ASTRAIOS — an interactive cosmic timeline.",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(health_router)
app.include_router(mission_router)

# ---------------------------------------------------------------------------
# WebSocket stub — placeholder for real-time mission chat
# ---------------------------------------------------------------------------


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Stub WebSocket that echoes messages back prefixed with "ASTRAIOS: ".
    Will be replaced with actual CrewAI / RAG-powered chat later.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"ASTRAIOS: {data}")
    except WebSocketDisconnect:
        pass  # client disconnected — nothing to clean up yet
