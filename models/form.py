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
    def get_crypto_data(currency = Form(...), price = Form(...), total_amount = Form(...), date = Form(...)):
        return AddCrypto(currency=currency, price=price, total_amount=total_amount, date=date)