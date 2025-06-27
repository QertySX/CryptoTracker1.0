from fastapi import Form
from models.schemas import UsersRegistration, UserLogin, AddCrypto


class GetForm:
    @staticmethod
    def register_form(username: str = Form(...),email: str = Form(...),password: str = Form(...)):
        return UsersRegistration(username=username, email=email, password=password)


    @classmethod
    def login_form(self, username: str = Form(...), password: str = Form(...)):
        return UserLogin(username=username, password=password)


class GetPortfolioForm:
    @staticmethod
    def get_crypto_data(currency: str = Form(...), price: str = Form(...), total_amount: str = Form(...)):
        return AddCrypto(currency=currency, price=price, total_amount=total_amount)