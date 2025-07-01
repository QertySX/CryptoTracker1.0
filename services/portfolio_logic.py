from models.models import Portfolio
import asyncio
from create_db import async_session
from sqlalchemy.future import select
from services.crypto_logic import GetCryptoData, SortAllCrypto
import logging


logging.basicConfig(level=logging.INFO)


class ProfitLoss:
    async def all_time_profit(self, user_id):
        async with async_session() as session:
            result = await session.execute(select(Portfolio).where(Portfolio.user_id == user_id))
            portfolio = result.scalars().all()

            fetcher = GetCryptoData()
            raw_crypto = await fetcher.fetch()
            strategy = SortAllCrypto()  
            crypto_data = strategy.get_current_price(raw_crypto)

            total_profit = 0

            for crypto_name, data in crypto_data.items():
                crypto_name_api = crypto_name
                current_price = data['price']

                for data in portfolio:
                    crypto_name_db = data.crypto_currency
                    buy_price = data.buy_price
                    total_amount = data.total_amount

                    # Профит = (Текущая цена - Цена покупки) × Количество токенов
                    if crypto_name_api.lower() == crypto_name_db.lower():
                        profit_or_loss = (current_price - buy_price) * total_amount
                        logging.info('')
                        logging.info('------------------')
                        logging.info(f'ID пользователя в базе: {user_id}')
                        logging.info(f'Название в базе: {crypto_name_db}')
                        logging.info(f'Название в апи: {crypto_name_api}')
                        logging.info(f'Такущая цена: {current_price}')
                        logging.info(f'Цена покупки: {buy_price}')
                        logging.info(f'Общее количество: {total_amount}')
                        logging.info('------------------')

                        total_profit += profit_or_loss
            return total_profit


class Balance:
    async def total_balance(self, user_id):
        async with async_session() as session:
            result = await session.execute(select(Portfolio).where(Portfolio.user_id == user_id))
            portfolio = result.scalars().all()


            total_spent = 0
            for data in portfolio:
                buy_price = data.buy_price
                total_amount = data.total_amount
                total_spent += buy_price * total_amount
            return total_spent    


class AveragePrice:
    async def average(self, user_id):
        async with async_session() as session:
            result = await session.execute(select(Portfolio).where(Portfolio.user_id == user_id))
            portfolio = result.scalars().all()

            avarge_buy_price = 0
            for data in portfolio:
                amount = data.total_amount
                price = data.buy_price
                avarge_buy_price += price * amount / amount
            return avarge_buy_price
        


