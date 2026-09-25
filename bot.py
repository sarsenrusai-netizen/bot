import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from dotenv import load_dotenv

# Загружаем переменные окружения из .env (если файл присутствует)

# Получаем токен бота из переменных окружения
BOT_TOKEN = "8776746316:AAFT0iXO4Rx9XSwGqUnrIkvLZ18aeU0iaGg"
# Инициализируем роутер
router = Router()


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Формирует главную Reply-клавиатуру."""
    kb = [
        [KeyboardButton(text="О нас"), KeyboardButton(text="Направления")],
        [KeyboardButton(text="Контакты")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


# --- Обработчики команд и кнопок ---


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработка команды /start."""
    welcome_text = (
        f"Здравствуйте, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в информационный бот для жителей и гостей "
        "города Петропавловск! 🏙\n\n"
        "Используйте кнопки меню ниже, чтобы узнать больше о нашем городе, "
        "популярных направлениях и контактах."
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@router.message(F.text == "О нас")
async def process_about(message: Message):
    """Информация о городе / проекте."""
    about_text = (
        "ℹ️ **О Петропавловске**\n\n"
        "Петропавловск — административный центр Северо-Казахстанской области, "
        "город с богатой историей, основанный в 1752 году.\n\n"
        "Наш проект создан для того, чтобы помочь жителям и гостям города "
        "быстро находить актуальную информацию, интересные места, туристические "
        "маршруты и нужные контакты."
    )
    await message.answer(about_text, parse_mode="Markdown")


@router.message(F.text == "Направления")
async def process_destinations(message: Message):
    """Основные направления и места."""
    destinations_text = (
        "🧭 **Популярные направления:**\n\n"
        "1. **Культура и история:**\n"
        "   • Историко-краеведческий музей\n"
        "   • Музейный комплекс «Резиденция Абылай хана»\n"
        "   • Областной русский драматический театр им. N. Погодина\n\n"
        "2. **Прогулки и отдых:**\n"
        "   • Улица Конституции Казахстана (одна из самых длинных пешеходных улиц в мире)\n"
        "   • Парк культуры и отдыха им. Первого Президента\n"
        "   • Набережная реки Есиль (Ишим)\n\n"
        "3. **Природа и туризм:**\n"
        "   • Загородные зоны отдыха и сосновые боры Приишимья"
    )
    await message.answer(destinations_text, parse_mode="Markdown")


@router.message(F.text == "Контакты")
async def process_contacts(message: Message):
    """Контактная информация."""
    contacts_text = (
        "📞 **Контакты и полезная информация:**\n\n"
        "• **Горячая линия акимата:** 109 (iKomek)\n"
        "• **Справочная автовокзала:** +7 (7152) 33-14-82\n"
        "• **Справочная ж/д вокзала:** 105\n\n"
        "📩 **Для связи с администрацией бота:**\n"
        "Email: info@petropavl-bot.kz\n"
        "Telegram: @petropavl_admin_support"
    )
    await message.answer(contacts_text, parse_mode="Markdown")


# --- Запуск бота ---


async def main():
    if not BOT_TOKEN:
        logging.error("Ошибка: Переменная окружения BOT_TOKEN не установлена!")
        sys.exit(1)

    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутер с хэндлерами
    dp.include_router(router)

    # Пропускаем накопившиеся накопившиеся обновления и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, stream=sys.stdout
    )
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
