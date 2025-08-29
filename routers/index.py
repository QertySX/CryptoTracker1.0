from fastapi import APIRouter, Request, status, Depends, Response
from typing import Annotated
from fastapi.responses import RedirectResponse
from services.crypto_logic import GetCryptoData, SortAllCrypto, FindCrypto
from fastapi.templating import Jinja2Templates
from services.auth_logic import get_current_active_user, get_current_user_for_page
from models.schemas import UserS
from jose import jwt, JWTError
import logging


logging.basicConfig(level=logging.INFO)
templates = Jinja2Templates(directory="templates")
home_router = APIRouter()


@home_router.get('/home', name="home")
async def index(request: Request, user: Annotated[UserS, Depends(get_current_user_for_page)]):
    fetcher = GetCryptoData()
    raw_crypto = await fetcher.fetch()

    strategy = SortAllCrypto()
    sorted_crypto = strategy.sort(raw_crypto)

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "data": sorted_crypto,
        "user": user
    })


@home_router.get('/search')
async def find_crypto(request: Request, crypto_name: str):
    fetcher = GetCryptoData()
    raw_crypto = await fetcher.fetch()

    strategy = SortAllCrypto()
    sorted_crypto = strategy.sort(raw_crypto)

    finder = FindCrypto()
    find_crypto = finder.find(crypto_name, sorted_crypto)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "data": find_crypto
        })


@home_router.get('/logout', name='logout')
async def logout(response: Response):
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="access_token")
    return response

