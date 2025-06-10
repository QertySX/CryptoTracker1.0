from fastapi import APIRouter, Request
from services.crypto_logic import GetCryptoData, SortAllCrypto, FindCrypto
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
crypto_router = APIRouter()

@app.get
@crypto_router.get('/')
async def index(request: Request):
    fetcher = GetCryptoData()
    raw_crypto = await fetcher.fetch()

    strategy = SortAllCrypto()
    sorted_crypto = strategy.sort(raw_crypto)
    return templates.TemplateResponse("index.html", {"request": request, "data": sorted_crypto})


@app.get
@crypto_router.get('/search')
async def find_crypto(request: Request, crypto_name: str):
    fetcher = GetCryptoData()
    raw_crypto = await fetcher.fetch()

    strategy = SortAllCrypto()
    sorted_crypto = strategy.sort(raw_crypto)

    finder = FindCrypto()
    find_crypto = finder.find(crypto_name, sorted_crypto)

    return templates.TemplateResponse("index.html", {"request": request, "data": find_crypto})
