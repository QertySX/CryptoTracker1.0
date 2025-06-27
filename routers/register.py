from fastapi import APIRouter, Request, Depends
from crud.users_crud import AddUser
from fastapi.templating import Jinja2Templates
from models.schemas import UsersRegistration
from fastapi.responses import RedirectResponse
from models.form import GetForm

 
templates = Jinja2Templates(directory="templates")
reg_router = APIRouter()

# Registration
@reg_router.get('/register', name='register')
async def show_register_form(request: Request):
    return templates.TemplateResponse("register_user.html", {"request": request})

@reg_router.post('/register')
async def register_users(user: UsersRegistration = Depends(GetForm.register_form)):
    new_user = AddUser(username=user.username, email=user.email, password_hash=user.password)
    await new_user.execute()
    return RedirectResponse(url="/login", status_code=302)





