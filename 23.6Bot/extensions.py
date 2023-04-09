#Для отправки запросов к API описать класс со статическим методом get_price(),
# который принимает три аргумента: имя валюты, цену на которую надо узнать,  —  base, имя валюты, цену в которой надо узнать,
# — quote, количество переводимой валюты — amount и возвращает нужную сумму в валюте.
import requests
import json
from config import keys

class GetPrice:
    @staticmethod
    def get_price(quote: str,base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount

class APIException(Exception):
    pass

