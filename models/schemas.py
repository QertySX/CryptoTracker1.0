from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsersRegistration(BaseModel):
    ''' 1. Разобраться с Pydantic для Users'''

    username = str
    email = EmailStr
    password_hash = str