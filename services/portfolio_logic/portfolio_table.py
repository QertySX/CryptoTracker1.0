from models.models import Portfolio
from create_db import async_session
from sqlalchemy.future import select
from services.crypto_logic import GetCryptoData, SortAllCrypto
import logging

logging.basicConfig(level=logging.INFO)


class PortfolioTable:

    async def average(self, portfolio) -> dict[str, float]:
        """Средняя цена покупки по каждому токену"""
        crypto_totals = {}

        for item in portfolio:
            name = item.crypto_currency.lower()
            amount = item.total_amount
            price = item.buy_price

            if name not in crypto_totals:
                crypto_totals[name] = {'total_amount': 0, 'total_spent': 0}

            crypto_totals[name]['total_amount'] += amount
            crypto_totals[name]['total_spent'] += price * amount

        return {
            name: (data['total_spent'] / data['total_amount']
                   if data['total_amount'] > 0 else 0)
            for name, data in crypto_totals.items()
        }

    async def holding_tokens(self, portfolio) -> dict[str, float]:
        """Сколько токенов держит пользователь"""
        holdings = {}
        for data in portfolio:
            name = data.crypto_currency.lower()
            holdings[name] = holdings.get(name, 0) + data.total_amount
        return holdings

    async def crypto_data_from_api(self) -> dict:
        """Данные из API (ключи приводим к lower)"""
        fetcher = GetCryptoData()
        crypto_from_api = SortAllCrypto()
        raw_crypto = await fetcher.fetch()
        api = crypto_from_api.crypto_portfolio_page(raw_crypto) or {}
        # Ключи -> lower
        return {str(k).lower(): v for k, v in api.items()}

    async def profit_or_loss(self, portfolio, crypto_data) -> dict[str, float]:
        """Прибыль/убыток по каждому токену (ключи уже в lower)"""
        profit_loss_for_crypto = {}

        for name_lc, api_data in crypto_data.items():
            current_price = api_data.get('price')
            if current_price is None:
                continue

            for entry in portfolio:
                if name_lc == entry.crypto_currency.lower():
                    pl = (current_price - entry.buy_price) * entry.total_amount
                    profit_loss_for_crypto[name_lc] = profit_loss_for_crypto.get(name_lc, 0) + pl

        return profit_loss_for_crypto


class SummaryBlock:
    async def all_time_profit(self, portfolio) -> float:
        """Общая прибыль/убыток по портфелю"""
        fetcher = GetCryptoData()
        raw_crypto = await fetcher.fetch()
        strategy = SortAllCrypto()
        crypto_data = strategy.get_current_price(raw_crypto)

        total_profit = 0

        for crypto_name, crypto_info in crypto_data.items():
            if not isinstance(crypto_info, dict) or 'price' not in crypto_info:
                continue

            current_price = crypto_info['price']

            for item in portfolio:
                if crypto_name.lower() == item.crypto_currency.lower():
                    profit_or_loss = (current_price - item.buy_price) * item.total_amount
                    total_profit += profit_or_loss

        return total_profit

    async def total_balance(self, portfolio) -> float:
        """Общая сумма вложений"""
        return sum(item.buy_price * item.total_amount for item in portfolio)


# --- Таблица + сводка ---
async def all_data_table(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Portfolio).where(Portfolio.user_id == user_id)
        )
        portfolio = result.scalars().all()

    if not portfolio:
        return {"data_table": {}, "summary": {"total_balance": 0, "all_time_profit": 0}}

    # расчёты по токенам
    table = PortfolioTable()
    crypto = await table.crypto_data_from_api()
    hold = await table.holding_tokens(portfolio)
    average = await table.average(portfolio)
    profit_loss_for_crypto = await table.profit_or_loss(portfolio, crypto)

    # таблица по каждой монете
    data_table = {}
    for entry in portfolio:
        name = entry.crypto_currency.lower()
        if name in crypto:
            crypto_data_api = crypto.get(name, {})
            data_table[name] = {
                'price': crypto_data_api.get('price'),
                'percent_change_1h': crypto_data_api.get('percent_change_1h'),
                'percent_change_24h': crypto_data_api.get('percent_change_24h'),
                'percent_change_7d': crypto_data_api.get('percent_change_7d'),
                'hold': hold.get(name, 0),
                'average': average.get(name, 0),
                'profit_loss': profit_loss_for_crypto.get(name, 0)
            }

    # итоговые суммы
    summary = SummaryBlock()
    total_balance = await summary.total_balance(portfolio)
    all_time_profit = await summary.all_time_profit(portfolio)

    result = {
        "data_table": data_table,
        "summary": {
            "total_balance": total_balance,
            "all_time_profit": all_time_profit
        }
    }

    logging.info(f"ALL DATA: {result}")
    return result
