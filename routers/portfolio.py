from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from typing import Annotated
from models.schemas import UserS
from models.form import GetPortfolioForm
from services.auth_logic import get_current_user_from_cookie, get_current_user_for_page

templates = Jinja2Templates(directory="templates")
portfolio_route = APIRouter()


@portfolio_route.get('/portfolio', name="portfolio")
async def portfolio(request: Request, response: Response, 
    current_user: Annotated[UserS, Depends(get_current_user_from_cookie)], 
    user: Annotated[UserS, Depends(get_current_user_for_page)]
    ):
    return templates.TemplateResponse("portfolio.html", {
        "request": request,
        'user': user
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
async def portfolio_process(request: Request, crypto_data: GetPortfolioForm = Depends(GetPortfolioForm.get_crypto_data)):
    pass