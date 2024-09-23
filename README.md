TG02_foto_audio_echo

## Этот бот для Telegram позволяет пользователям:

    Сохранять отправленные фото в папку img.
    Переводить текст на выбранный язык с голосовым дублированием.
    Выбирать язык перевода.
    Получать помощь по использованию бота через команду /help или кнопку "🆘 Помощь".

### Особенности

    Сохранение фото: Бот сохраняет все фотографии, отправленные пользователями, с уникальными именами файлов.
    Перевод текста: Переводит введенный текст на выбранный язык и отправляет голосовое сообщение с озвучкой перевода.
    Выбор языка: Пользователи могут выбирать язык для перевода из списка доступных языков.
    Голосовое дублирование: Использует gTTS для создания голосового сообщения с переведенным текстом.
    Удобный интерфейс: Интерактивные кнопки для легкого взаимодействия с ботом.

### Требования

    Python 3.6 или выше
    Telegram Bot Token (полученный от BotFather)

### Установка

- #### Клонируйте репозиторий или скачайте файлы бота:

```
git clone https://github.com/yourusername/yourbotrepository.git
```

- #### Перейдите в директорию с ботом:

```
cd yourbotrepository
```

- #### Создайте виртуальное окружение (рекомендуется):

```
    python3 -m venv venv
    source venv/bin/activate  # Для Unix/Linux
    venv\Scripts\activate     # Для Windows
```
- #### Установите зависимости:

```
    pip install -r requirements.txt
```
- #### Настройка
```
    Получите токен вашего бота от BotFather в Telegram.

    Откройте файл бота (например, bot.py) и замените 'YOUR_BOT_TOKEN_HERE' на токен вашего бота:

    python

    API_TOKEN = 'ВАШ_ТОКЕН_БОТА_ЗДЕСЬ'
```

Запуск бота

    Убедитесь, что вы находитесь в виртуальном окружении (если создавали его).

Запустите бота:

```
    python bot.py
```
Или, если ваш файл называется иначе:

```
    python your_bot_file_name.py
```
Бот теперь работает и готов принимать сообщения в Telegram.

### Использование
- #### Команды
```
    /start - Начать работу с ботом. Отправляет приветственное сообщение и отображает основные функции.
    /help - Получить справку по использованию бота.
```
- #### Кнопки
```
    📷 Загрузить фото: Нажмите, чтобы отправить фото боту. Фото будет сохранено в папке img.
    🔤 Перевести текст: Нажмите, чтобы отправить текст для перевода на выбранный язык с голосовым дублированием.
    🌐 Выбрать язык: Нажмите, чтобы выбрать язык перевода из списка доступных.
    🆘 Помощь: Нажмите, чтобы получить справку по использованию бота.
```
- #### Процесс использования
```
- Сохранение фото:
    Нажмите кнопку 📷 Загрузить фото.
    Отправьте фото в ответ на сообщение бота.
    Бот сохранит фото и подтвердит сохранение.
```
```
- Перевод текста с голосовым дублированием:
    Нажмите кнопку 🔤 Перевести текст.
    Отправьте текст, который хотите перевести.
    Бот переведет текст на выбранный язык и отправит голосовое сообщение с озвучкой.
```
```
- Выбор языка перевода:
    Нажмите кнопку 🌐 Выбрать язык.
    Выберите язык из предложенного списка.
    Бот подтвердит выбор языка.
```
```
- Получение помощи:
    Нажмите кнопку 🆘 Помощь или отправьте команду /help.
    Бот отправит справочное сообщение с инструкциями.
```
- #### Настройка доступных языков

Вы можете изменить или расширить список доступных языков для перевода и озвучивания, отредактировав словарь available_languages в коде бота:

```
available_languages = {
    'en': 'Английский',
    'ru': 'Русский',
    'es': 'Испанский',
    'de': 'Немецкий',
    'fr': 'Французский',
    # Добавьте другие языки по желанию
}
```

- #### Убедитесь, что выбранные языки поддерживаются библиотеками googletrans и gTTS.
```
- Ограничения

    Длина текста для озвучивания: Из-за ограничений gTTS, максимальная длина текста для озвучивания составляет около 200 символов.
    Сохранение настроек: Выбранный язык сохраняется только на время работы бота. Если бот перезапускается, настройки сбрасываются.
```
```
- Возможные проблемы

    Ошибка при переводе: Если возникает ошибка при переводе текста, убедитесь, что текст введен корректно и что у вас есть доступ к сервисам Google Translate.
    Ошибка при создании голосового сообщения: Может возникать из-за неподдерживаемого языка или проблем с gTTS.
```
- #### Лицензия

Этот проект находится под лицензией MIT. Подробности в файле LICENSE.