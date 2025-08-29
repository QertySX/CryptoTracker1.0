from create_db import async_session
from models.models import Portfolio, User
import logging
from sqlalchemy import func, delete, update


logging.basicConfig(level=logging.INFO)


class AddCryptoInDb:
    def __init__(self, crypto_currency, buy_price, total_amount, date, user_id):
        self.crypto_currency = crypto_currency
        self.buy_price = buy_price
        self.total_amount = total_amount
        self.date = date
        self.user_id = user_id

    async def execute(self):
        try:
            async with async_session() as session:
                crypto_data = Portfolio(
                    crypto_currency = self.crypto_currency,
                    buy_price = self.buy_price,
                    total_amount = self.total_amount,
                    date = self.date,
                    user_id = self.user_id
                )
                session.add(crypto_data)
                await session.commit()
                return crypto_data
        except Exception as e:
            logging.error(f'[INFO] Ошибка {e}')


class DeleteCryptoInDb:
    def __init__(self, crypto_currency: str, user_id: int):
        self.crypto_currency = crypto_currency
        self.user_id = user_id

    async def execute(self):
        try:
            async with async_session() as session:
                delete_data = delete(Portfolio).where(
                    func.lower(Portfolio.crypto_currency) == self.crypto_currency.lower(),
                    Portfolio.user_id == self.user_id
                )
                await session.execute(delete_data)
                await session.commit()
        except Exception as e:
            logging.error(f'[INFO] Ошибка при удалении криптовалюты: {e}')


class EditCryptoInDb:
    def __init__(self, crypto_currency: str, user_id: int, total_amount: float, buy_price: float):
        self.crypto_currency = crypto_currency
        self.total_amount = total_amount
        self.user_id = user_id
        self.buy_price = buy_price

    async def execute(self):
        try:
            async with async_session() as session:
                edit_crypto = (
                    update(Portfolio)
                    .where(func.lower(Portfolio.crypto_currency) == self.crypto_currency.lower(), Portfolio.user_id == self.user_id)
                    .values(total_amount=self.total_amount, buy_price=self.buy_price))

                await session.execute(edit_crypto)
                await session.commit()
        except Exception as e:
            logging.error(f'[INFO] Ошибка при удалении криптовалюты: {e}')
