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


class SortAllCrypto:
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


    def get_current_price(self, data: dict) -> dict:
        '''Фильтрация данных по name, price'''
        try:
            crypto_data = dict()
            if 'data' not in data:
                return {"error": "Данные не получены"}
            for crypto in data['data']:
                necessary_data = {
                    "price": crypto['quote']['USD']['price'],
                }
                crypto_data[crypto['name']] = necessary_data
            return crypto_data

        except Exception as e:
            logging.error(f'[INFO] error {e}')


    def crypto_portfolio_page(self, data) -> dict:
        '''Фильтрация данных по Name, Price, 1h%, 24h%, 7d%, Holdings, Avg.BuyPrice, Profit/Loss, Actions'''
        try:
            crypto_data = dict()
            if 'data' not in data:
                return {"error": "Данные не получены"}
            for crypto in data['data']:
                necessary_data = {
                    "price": crypto['quote']['USD']['price'],
                    "percent_change_1h": crypto['quote']['USD']['percent_change_1h'],
                    "percent_change_24h": crypto['quote']['USD']['percent_change_24h'],
                    "percent_change_7d": crypto['quote']['USD']['percent_change_7d'],
                }
                crypto_data[crypto['name']] = necessary_data
            return crypto_data
        except Exception as e:
            logging.error(f'[INFO] error {e}')
        


class FindCrypto:
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



