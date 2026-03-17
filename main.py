import asyncio
import os
import shutil
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.scheduler import PriceScheduler
from app.api import setup_routes

# ── Path resolution: normal run vs PyInstaller frozen bundle ──────────────────
if getattr(sys, "frozen", False):
    _BUNDLE_DIR = sys._MEIPASS                          # extracted bundle (read-only)
    _EXE_DIR    = os.path.dirname(sys.executable)       # dir next to the .exe (writable)
    # Copy default config next to the exe on first launch so the user can edit it
    _cfg_src = os.path.join(_BUNDLE_DIR, "config.yaml")
    _cfg_dst = os.path.join(_EXE_DIR,    "config.yaml")
    if not os.path.exists(_cfg_dst):
        shutil.copy(_cfg_src, _cfg_dst)
    CONFIG_PATH = _cfg_dst
    STATIC_DIR  = os.path.join(_BUNDLE_DIR, "static")
else:
    _HERE       = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(_HERE, "config.yaml")
    STATIC_DIR  = os.path.join(_HERE, "static")
# ─────────────────────────────────────────────────────────────────────────────

scheduler = PriceScheduler(config_path=CONFIG_PATH)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

router = APIRouter()
setup_routes(router, scheduler, CONFIG_PATH)
app.include_router(router)

@app.get("/")
async def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

def _free_port(start: int = 8000) -> int:
    import socket
    for port in range(start, start + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    return start

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 0)) or _free_port(8000)
    print(f"\n  Binance Price Alert → http://localhost:{port}\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
