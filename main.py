from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from routers.crypto import crypto_router


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(crypto_router, prefix="")
app.include_router(crypto_router, prefix="/search", tags=["search"])