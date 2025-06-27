from fastapi import APIRouter, Request, Response, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from models.form import GetForm
from services.auth_logic import authenticate_user, create_access_token
from fastapi.responses import RedirectResponse
from config import ACCESS_TOKEN_EXPIRE


auth_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@auth_router.get('/login', name='auth')
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login")
async def login_process(response: Response, user: GetForm = Depends(GetForm.login_form)):
    user = await authenticate_user(user.username, user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/home", status_code=302)

    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token}", 
        httponly=True, 
        max_age=ACCESS_TOKEN_EXPIRE)
    return  response

