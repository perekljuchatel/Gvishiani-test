# bot.py

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Импортируем наш токен и URL API
from config import TELEGRAM_BOT_TOKEN, QUOTE_API_URL
# Импортируем нашу функцию для получения цитат
from quote_api import get_random_quote

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING) # Убираем лишние логи от httpx
logger = logging.getLogger(__name__)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение при вызове команды /start."""
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я бот, который может присылать тебе случайные цитаты. "
        "Попробуй команду /quote."
    )

# Обработчик команды /quote
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет случайную цитату."""
    logger.info("Получена команда /quote")
    # Получаем цитату, используя нашу функцию из quote_api.py
    quote_text = await get_random_quote(QUOTE_API_URL)
    await update.message.reply_text(quote_text)
    logger.info(f"Отправлена цитата: {quote_text[:50]}...") # Логируем первые 50 символов

# Основная функция, которая запускает бота
def main() -> None:
    """Запускает бота."""
    # Создаем объект Application и передаем токен вашего бота.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quote", quote))

    # Запускаем бота (начинаем опрос новых обновлений)
    logger.info("Бот запущен. Ожидаю команд...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()