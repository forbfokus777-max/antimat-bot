import logging
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Включаем логирование (опционально, но полезно для отладки)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Список запрещённых слов (можно расширить)
MAT_WORDS = {
    'бля', 'блядь', 'сука', 'пизда', 'хуй', 'ебать', 'ёбать', 'нахуй', 'нахер',
    'пидор', 'пидр', 'гандон', 'дрочить', 'мудак', 'ублюдок', 'сучара'
}

# Функция для проверки наличия мата
def contains_mat(text: str) -> bool:
    text = text.lower()
    for word in MAT_WORDS:
        # Используем регулярное выражение, чтобы ловить слово целиком (с учётом окончаний и знаков)
        if re.search(rf'\b{re.escape(word)}\w*', text, re.IGNORECASE):
            return True
    return False

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    if contains_mat(message.text):
        try:
            await message.delete()
            # Опционально: отправить предупреждение в ЛС
            # await context.bot.send_message(
            #     chat_id=message.from_user.id,
            #     text="Пожалуйста, не используйте ненормативную лексику в чате."
            # )
        except Exception as e:
            logging.warning(f"Не удалось удалить сообщение: {e}")

# Основная функция
def main():
    # Вставьте сюда токен вашего бота
    TOKEN = '7924907918:AAEavjpYh75rZLAA9tsXARqL8Trdw6BVLJI'

    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчик для всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
