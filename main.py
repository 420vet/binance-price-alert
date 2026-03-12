import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.scheduler import PriceScheduler
from app.api import setup_routes

CONFIG_PATH = "config.yaml"
scheduler = PriceScheduler(config_path=CONFIG_PATH)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

router = APIRouter()
setup_routes(router, scheduler, CONFIG_PATH)
app.include_router(router)

@app.get("/")
async def index():
    return FileResponse("static/index.html")
