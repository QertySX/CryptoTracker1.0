from fastapi import APIRouter, Request
from crud.users_crud.py import AddUserCommand
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
reg_router = APIRouter()

@app.get
@reg_router.get('register')
async def register_users():
    ''' 1. Дописать параметры с pydantic
        2. Доделать регистрацию 
        3. Захешировать пароль
    '''
    pass