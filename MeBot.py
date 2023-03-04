import logging
import openai
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Устанавливаем уровень логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Получаем токен API бота
TOKEN = "ваш"

# Получаем API ключ от OpenAI
OPENAI_API_KEY = "ваш"

# Создаем объект updater и передаем ему токен API бота
updater = Updater(TOKEN, use_context=True)

# Получаем объект диспетчера сообщений
dispatcher = updater.dispatcher

# Напишите функцию-обработчик для команды /start
def start(update: Update, context: telegram.ext.CallbackContext) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text="Привет, я бот для общения с GPT-чатом!")

# Регистрируем обработчик команды /start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Напишите функцию-обработчик для текстовых сообщений
def respond(update: Update, context: telegram.ext.CallbackContext) -> None:
    # Получаем текст сообщения от пользователя
    user_message = update.message.text

    # Отправляем запрос в OpenAI API, чтобы получить ответ на сообщение
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=user_message, max_tokens=1024, n=1, stop=None, temperature=0.7,
    )
    # Получаем ответ от модели GPT
    gpt_response = response.choices[0].text.strip()

    # Отправляем ответ обратно в чат Telegram
    context.bot.send_message(chat_id=update.message.chat_id, text=gpt_response)

# Регистрируем обработчик текстовых сообщений
respond_handler = MessageHandler(Filters.text & (~Filters.command), respond)
dispatcher.add_handler(respond_handler)

# Запускаем бота
updater.start_polling()
