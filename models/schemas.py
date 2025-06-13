from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsersRegistration(BaseModel):

    username = str
    email = EmailStr
    password_hash = str