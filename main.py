import os
import logging
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator
from gtts import gTTS

# Установите уровень логирования
logging.basicConfig(level=logging.INFO)

# Токен вашего бота
API_TOKEN = '8186888870:AAF4WaEsgE3qUxN4nPgOQxzol0AouJqHSw8'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Создаем папки, если они не существуют
if not os.path.exists('img'):
    os.makedirs('img')
if not os.path.exists('voice'):
    os.makedirs('voice')

# Инициализация переводчика
translator = Translator()

# Создаем клавиатуру с кнопками
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_photo = KeyboardButton('📷 Загрузить фото')
button_translate = KeyboardButton('🔤 Перевести текст')
button_select_lang = KeyboardButton('🌐 Выбрать язык')
button_help = KeyboardButton('🆘 Помощь')
keyboard.add(button_photo, button_translate)
keyboard.add(button_select_lang, button_help)

# Словарь для хранения выбранного языка каждого пользователя
user_language = {}

# Счетчики для имен файлов
photo_counter = {}
voice_counter = {}

# Список доступных языков
available_languages = {
    'en': 'Английский',
    'ru': 'Русский',
    'es': 'Испанский',
    'de': 'Немецкий',
    'fr': 'Французский',
    # Добавьте другие языки по желанию
}

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_language[message.from_user.id] = 'en'  # Устанавливаем английский по умолчанию
    await message.reply(
        "Привет! Я могу сохранить ваше фото и перевести текст на выбранный вами язык с голосовым дублированием.",
        reply_markup=keyboard
    )
    # Отправляем голосовое сообщение
    tts = gTTS(text="Здравствуйте! Я ваш бот-помощник.", lang='ru')
    tts.save("voice_message.ogg")
    with open("voice_message.ogg", 'rb') as voice:
        await bot.send_voice(chat_id=message.chat.id, voice=voice)
    os.remove("voice_message.ogg")

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = (
        "🆘 *Справка по боту:*\n\n"
        "• Нажмите кнопку 📷 *Загрузить фото*, чтобы отправить фото и сохранить его.\n"
        "• Нажмите кнопку 🔤 *Перевести текст*, чтобы отправить текст для перевода на выбранный язык с голосовым "
        "дублированием.\n"
        "• Нажмите кнопку 🌐 *Выбрать язык*, чтобы изменить язык перевода.\n"
        "• Нажмите кнопку 🆘 *Помощь*, чтобы увидеть это сообщение.\n"
        "• Вы также можете использовать команды:\n"
        "  - /start - начать работу с ботом.\n"
        "  - /help - показать это сообщение помощи.\n"
    )
    await message.reply(help_text, parse_mode='Markdown', reply_markup=keyboard)

# Обработчики нажатий на кнопки
@dp.message_handler(lambda message: message.text == '📷 Загрузить фото')
async def prompt_photo(message: types.Message):
    await message.reply("Пожалуйста, отправьте мне фото, и я сохраню его.")

@dp.message_handler(lambda message: message.text == '🔤 Перевести текст')
async def prompt_text(message: types.Message):
    await message.reply("Пожалуйста, отправьте мне текст, и я переведу его на выбранный язык с голосовым дублированием.")

@dp.message_handler(lambda message: message.text == '🆘 Помощь')
async def handle_help_button(message: types.Message):
    await send_help(message)

@dp.message_handler(lambda message: message.text == '🌐 Выбрать язык')
async def select_language(message: types.Message):
    # Создаем встроенную клавиатуру с доступными языками
    inline_kb = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=lang_name, callback_data=f"lang_{lang_code}")
        for lang_code, lang_name in available_languages.items()
    ]
    inline_kb.add(*buttons)
    await message.reply("Пожалуйста, выберите язык для перевода:", reply_markup=inline_kb)

# Обработчик выбора языка
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('lang_'))
async def process_language_selection(callback_query: types.CallbackQuery):
    lang_code = callback_query.data[5:]  # Извлекаем код языка
    user_language[callback_query.from_user.id] = lang_code  # Сохраняем выбранный язык
    lang_name = available_languages.get(lang_code, 'неизвестный язык')
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали язык: {lang_name}", reply_markup=keyboard)

# Обработчик фото с более коротким именем файла
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    # Инициализируем счетчик для пользователя, если его еще нет
    if user_id not in photo_counter:
        photo_counter[user_id] = 1
    else:
        photo_counter[user_id] += 1

    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    downloaded_file = await bot.download_file(file_path)
    # Генерируем более короткое имя файла
    file_name = f'img/photo_{user_id}_{photo_counter[user_id]}.jpg'
    with open(file_name, 'wb') as f:
        f.write(downloaded_file.getvalue())
    await message.reply("Фото сохранено!", reply_markup=keyboard)

# Обработчик текстовых сообщений с голосовым дублированием
@dp.message_handler(content_types=['text'])
async def handle_text(message: types.Message):
    text = message.text
    if text in ['📷 Загрузить фото', '🔤 Перевести текст', '🆘 Помощь', '🌐 Выбрать язык']:
        # Если это текст кнопок, не обрабатываем его как обычный текст
        return

    user_id = message.from_user.id
    target_lang = user_language.get(user_id, 'en')  # Получаем выбранный язык, по умолчанию английский

    # Переводим текст на выбранный язык
    try:
        translated = translator.translate(text, dest=target_lang)
    except Exception as e:
        await message.reply("Ошибка при переводе текста. Пожалуйста, попробуйте еще раз.")
        logging.error(f"Ошибка при переводе: {e}")
        return

    translated_text = translated.text

    # Отправляем текстовый перевод
    await message.reply(
        f"Перевод на {available_languages.get(target_lang, 'выбранный язык')}:\n{translated_text}",
        reply_markup=keyboard
    )

    # Генерируем голосовое сообщение с переведенным текстом
    # Инициализируем счетчик для голосовых сообщений
    if user_id not in voice_counter:
        voice_counter[user_id] = 1
    else:
        voice_counter[user_id] += 1

    # Разбиваем текст на части по 200 символов
    max_length = 200
    text_parts = [translated_text[i:i + max_length] for i in range(0, len(translated_text), max_length)]

    for index, part in enumerate(text_parts):
        # Создаем голосовое сообщение для каждой части
        try:
            tts = gTTS(text=part, lang=target_lang)
        except Exception as e:
            await message.reply("Ошибка при создании голосового сообщения. Пожалуйста, попробуйте еще раз.")
            logging.error(f"Ошибка при создании голосового сообщения: {e}")
            return

        voice_file_name = f'voice/voice_{user_id}_{voice_counter[user_id]}_{index}.ogg'
        tts.save(voice_file_name)

        # Отправляем голосовое сообщение
        with open(voice_file_name, 'rb') as voice:
            await bot.send_voice(chat_id=message.chat.id, voice=voice)

        # Удаляем файл после отправки
        os.remove(voice_file_name)

    # Увеличиваем счетчик голосовых сообщений
    voice_counter[user_id] += len(text_parts) - 1  # Уже увеличили на 1 ранее

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
