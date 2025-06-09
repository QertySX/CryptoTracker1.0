import asyncio
from config import api_key, url
import logging
import aiohttp


class GetCryptoData:
    ''' Метод который получает сырые данные через API CoinMarketCup'''
    def __init__(self):
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }
        self.url = url

    async def fetch(self):
        try: 
            logging.info("Получение данных криптовалюты...")
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers) as response:

                    if response.status == 200:
                        result = await response.json()
                        logging.info("[INFO] Данные в func_1 получены!")
                        return result
                    else:
                        logging.error(f'[INFO] Ошибка {response.status}')
                        return {f"[INFO] HTTP ошибка {response.status}"}
                        
        except Exception as e:
            logging.error(f'[INFO] Ошибка: {e}')


class SortStrategy:
    '''Стратегия сортировки'''
    def sort(self, data: dict) -> dict:
        raise NotImplementedError()


class SortAllCrypto(SortStrategy):
    '''Фильтрация данных по price, volume_24h, percent_change_24h, market_cap'''
    def sort(self, data: dict) -> dict:
        try:
            all_data = {}

            if 'data' not in data:
                return {"error": "Данные не получены"}

            for crypto in data['data']:
                necessary_data = {
                    "price": crypto['quote']['USD']['price'],
                    "volume_24h": crypto['quote']['USD']['volume_24h'],
                    "percent_change_24h": crypto['quote']['USD']['percent_change_24h'],
                    "market_cap": crypto['quote']['USD']['market_cap']
                }
                all_data[crypto['name']] = necessary_data
            return all_data
        except Exception as e:
            logging.error(f'[INFO] error {e}')

def apply_sort(data, strategy: SortStrategy):
    return strategy.sort(data)


class FinderStrategy:
    '''Стратегия поиска'''
    def find(self, name: str, data: dict) -> dict:
        raise NotImplementedError()


class FindCrypto(FinderStrategy):
    '''Поиск одной криптовалюты'''
    def find(self, name, data: dict) -> dict:
        try:
            filtered_data = dict()
            for crypto_name, crypto_data in data.items():
                if crypto_name.lower() == name.lower():
                    filtered_data[crypto_name] = crypto_data
                    break
            return filtered_data
        except Exception as e:
            logging.error(f'[INFO] error {e}')


def apply_find(name, data, strategy: FinderStrategy):
    return strategy.find(name, data)

