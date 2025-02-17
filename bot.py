# bot.py
import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Обработка команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = (
        "Привет! Я бот для конвертации валют.\n\n"
        "Чтобы узнать цену валюты, отправьте сообщение в формате:\n"
        "<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену> <количество>\n\n"
        "Пример: USD EUR 100\n\n"
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/help - помощь\n"
        "/values - список доступных валют"
    )
    bot.reply_to(message, instructions)

# Обработка команды /values
@bot.message_handler(commands=['values'])
def send_available_currencies(message):
    currencies = (
        "Доступные валюты:\n"
        "USD - Доллар США\n"
        "EUR - Евро\n"
        "RUB - Российский рубль"
    )
    bot.reply_to(message, currencies)

# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        # Разбиваем сообщение на части
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException("Неверный формат запроса. Используйте: <валюта1> <валюта2> <количество>.")

        base, quote, amount = parts
        amount = float(amount)

        # Получаем результат конвертации
        result = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)
        bot.reply_to(message, f"{amount} {base.upper()} = {result} {quote.upper()}")

    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
    except ValueError:
        bot.reply_to(message, "Ошибка: Неверное количество валюты. Укажите число.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)