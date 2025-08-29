from fastapi import Form
from models.schemas import UsersRegistration, UserLogin, AddCrypto, EditCrypto, DeleteCrypto


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


class DeleteCryptoForm:
    @staticmethod
    def delete_crypto(crypto_currency = Form(...)):
        return DeleteCrypto(crypto_currency=crypto_currency)


class EditCryptoForm:
    @staticmethod
    def edit_crypto(crypto_currency = Form(...), total_amount = Form(...), buy_price = Form(...)):
        return EditCrypto(crypto_currency=crypto_currency, total_amount=total_amount, buy_price=buy_price)