from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import Response
import httpx
from app.config import save_config

VALID_INTERVALS = {"1m","3m","5m","15m","30m","1h","2h","4h","6h","12h","1d"}
_LOGO_CDN = "https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/color/{sym}.svg"
_logo_cache: dict = {}

def setup_routes(router: APIRouter, scheduler, config_path: str):

    @router.get("/config")
    async def get_config():
        return scheduler.config

    @router.post("/config")
    async def post_config(data: dict):
        save_config(config_path, data)
        scheduler.reload()
        return {"status": "ok"}

    @router.get("/logo/{symbol}")
    async def get_logo(symbol: str):
        sym = symbol.lower().strip()
        if sym in _logo_cache:
            return Response(_logo_cache[sym], media_type="image/svg+xml",
                            headers={"Cache-Control": "public, max-age=86400"})
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                r = await client.get(_LOGO_CDN.format(sym=sym))
                if r.status_code == 200:
                    _logo_cache[sym] = r.content
                    return Response(r.content, media_type="image/svg+xml",
                                    headers={"Cache-Control": "public, max-age=86400"})
        except Exception:
            pass
        return Response(status_code=404)

    @router.get("/chart/{symbol}")
    async def get_chart(
        symbol: str,
        interval: str = Query(default="5m"),
        limit: int = Query(default=100, ge=10, le=500),
    ):
        iv = interval if interval in VALID_INTERVALS else "5m"
        return await scheduler.client.get_klines(symbol.upper(), iv, limit)

    @router.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        await scheduler.connect(ws)
        try:
            while True:
                await ws.receive_text()
        except WebSocketDisconnect:
            scheduler.disconnect(ws)
