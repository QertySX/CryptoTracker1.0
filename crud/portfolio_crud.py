from create_db import async_session
from models.models import Portfolio, User


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
            print(f'[INFO] Ошибка {e}')