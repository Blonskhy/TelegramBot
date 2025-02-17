# extensions.py
import requests
import json

# Собственное исключение для обработки ошибок
class APIException(Exception):
    pass

# Класс для работы с API валют
class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        # Проверяем, что валюты разные
        if base == quote:
            raise APIException(f"Невозможно перевести одинаковые валюты: {base}.")

        # Получаем курсы валют через API
        try:
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base}")
            data = json.loads(response.text)
            rate = data['rates'][quote]
        except KeyError:
            raise APIException(f"Валюта {base} или {quote} не найдена.")
        except Exception as e:
            raise APIException(f"Ошибка при запросе к API: {e}")

        # Вычисляем итоговую сумму
        return round(rate * amount, 2)