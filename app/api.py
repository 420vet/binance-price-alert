from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.config import save_config

def setup_routes(router: APIRouter, scheduler, config_path: str):

    @router.get("/config")
    async def get_config():
        return scheduler.config

    @router.post("/config")
    async def post_config(data: dict):
        save_config(config_path, data)
        scheduler.reload()
        return {"status": "ok"}

    @router.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        await scheduler.connect(ws)
        try:
            while True:
                await ws.receive_text()
        except WebSocketDisconnect:
            scheduler.disconnect(ws)
