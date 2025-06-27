from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer


class UsersRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str | None = None


class UserS(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None

    class Config:
        orm_mode = True


class AddCrypto(BaseModel):
    currency: str
    price: float
    total_amount: float








        