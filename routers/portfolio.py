from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from models.schemas import UserS
from models.form import GetPortfolioForm
from models.models import Portfolio
from services.auth_logic import get_current_user_from_cookie, get_current_user_for_page
from crud.portfolio_crud import AddCryptoInDb
from create_db import async_session
from services.portfolio_logic import Balance, AveragePrice, ProfitLoss
from sqlalchemy.future import select



templates = Jinja2Templates(directory="templates")
portfolio_route = APIRouter()


@portfolio_route.get('/portfolio', name="portfolio")
async def portfolio(request: Request, response: Response, 
    current_user: Annotated[UserS, Depends(get_current_user_from_cookie)], 
    user: Annotated[UserS, Depends(get_current_user_for_page)]
    ):
    
    balance = Balance()
    profit_loss = ProfitLoss()
    average_price = AveragePrice()

    total_balance = await balance.total_balance(current_user.id)
    all_time_profit = await profit_loss.all_time_profit(current_user.id)
    average_buy_price = await average_price.average(current_user.id)

    return templates.TemplateResponse("portfolio.html", {
        "request": request,
        'user': user,
        'total_balance': total_balance,
        'all_time_profit': all_time_profit,
        'avarge_buy_price': average_buy_price
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