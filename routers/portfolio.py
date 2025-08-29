from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from models.schemas import UserS, DeleteCrypto, EditCrypto
from models.form import GetPortfolioForm, EditCryptoForm, DeleteCryptoForm
from models.models import Portfolio
from services.auth_logic import get_current_user_from_cookie, get_current_user_for_page
from crud.portfolio_crud import AddCryptoInDb, DeleteCryptoInDb, EditCryptoInDb
from create_db import async_session
from services.portfolio_logic.portfolio_table import PortfolioTable, all_data_table, SummaryBlock
from sqlalchemy.future import select
from sqlalchemy import delete
import logging


logging.basicConfig(level=logging.INFO)
templates = Jinja2Templates(directory="templates")
portfolio_route = APIRouter()


@portfolio_route.get('/portfolio', name="portfolio")
async def portfolio(
    request: Request,
    response: Response,
    current_user: Annotated[UserS, Depends(get_current_user_from_cookie)], 
    user: Annotated[UserS, Depends(get_current_user_for_page)]
):
    all_data = await all_data_table(current_user.id)

    return templates.TemplateResponse("portfolio.html", {
        "request": request,
        "user": user,
        "data_table": all_data["data_table"],
        "all_time_profit": all_data["summary"]["all_time_profit"],
        "total_balance": all_data["summary"]["total_balance"]
    })



@portfolio_route.get("/portfolio/add")
async def show_add_form(request: Request, 
    current_user: Annotated[UserS, Depends(get_current_user_from_cookie)], 
    user: Annotated[UserS, Depends(get_current_user_for_page)],
    ):  
    return templates.TemplateResponse("add_portfolio.html", {
        "request": request,
        'user': user,
        })


@portfolio_route.post("/portfolio/add")
async def portfolio_process(request: Request, 
    crypto_data: GetPortfolioForm = Depends(GetPortfolioForm.get_crypto_data),
    user = Depends(get_current_user_from_cookie)
    ):
    add_portfolio = AddCryptoInDb(
        crypto_currency=crypto_data.currency, 
        buy_price=crypto_data.price, 
        total_amount=crypto_data.total_amount, 
        date=crypto_data.date, 
        user_id=user.id
        )
    await add_portfolio.execute()
    return RedirectResponse(url="/portfolio", status_code=302)


@portfolio_route.post('/portfolio', name="_delete")
async def _delete(
    request: Request, 
    user: Annotated[UserS, Depends(get_current_user_from_cookie)],
    delete_crypto: DeleteCrypto = Depends(DeleteCryptoForm.delete_crypto)
):
    deleter = DeleteCryptoInDb(crypto_currency=delete_crypto.crypto_currency, user_id=user.id)
    await deleter.execute()

    return RedirectResponse(url="/portfolio", status_code=302)


@portfolio_route.get('/portfolio/edit', name='edit')
async def show_edit_portfolio(request: Request,
    current_user: Annotated[UserS, Depends(get_current_user_from_cookie)], 
    user: Annotated[UserS, Depends(get_current_user_for_page)],
    ):
    return templates.TemplateResponse(
        "edit_portfolio.html",{
        "request": request,
        'user': user,
        })


@portfolio_route.post('/portfolio/edit', name='edit')
async def edit_crypto(
    request: Request, 
    user: Annotated[UserS, Depends(get_current_user_from_cookie)],
    edit_crypto: EditCrypto = Depends(EditCryptoForm.edit_crypto),
    ):
    
    edit = EditCryptoInDb(
        crypto_currency=edit_crypto.crypto_currency, 
        user_id=user.id,
        total_amount=edit_crypto.total_amount, 
        buy_price=edit_crypto.buy_price
    )
    await edit.execute()

    return RedirectResponse(url="/portfolio", status_code=302)