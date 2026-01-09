# SubsSpyBot
Бот для извлечения списка участников из JSON-экспорта истории Telegram-чатов.
## Быстрый запуск
### 1. Получите токен бота:
* Откройте @BotFather в Telegram
* Используйте `/mybots` → выберите бота → API Token
* Или создайте нового: `/newbot`
### 2. Настройте окружение:
```bash
echo "TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН" > .env
```
### 3. Запустите бота через Docker:
```bash
docker-compose up --build
```
## Архитектура
```html
project/
├── main.py                      # Точка входа
├── bot/                         # Слой взаимодействия с Telegram
│   ├── telegram_api.py         # HTTP-запросы к Bot API
│   └── core/                   # Логика бота
│       ├── handlers.py        # Обработчики команд и файлов
│       ├── dialog_manager.py  # Управление состояниями (FSM)
│       └── messages.py        # Текстовые шаблоны
├── core/orchestrator.py        # Координатор обработки
├── parsers/                    # Парсеры данных
│   └── telegram_json_parser.py # Парсинг JSON-экспорта
├── generators/                 # Генераторы результатов
│   ├── text_generator.py      # Текстовый вывод
│   └── excel_generator.py     # Excel-файлы (.xlsx)
├── models/subscriber.py       # Модель участника
├── contracts/                 # Абстрактные интерфейсы
└── utils/logging.py           # Настройка логирования
```
### Принципы работы:
1. Пользователь отправляет JSON-файлы → `Telegram API`
2. Бот загружает файлы в память → `telegram_api.py`
3. Оркестратор запускает парсинг → `orchestrator.py`
4. Парсер извлекает участников → `telegram_json_parser.py`
5. Генератор формирует результат → `text_generator.py / excel_generator.py`
6. Результат отправляется пользователю → `Telegram API`

## Использование
1. Экспортируйте историю чата в Telegram Desktop (формат JSON)
2. Отправьте файл боту в чат (макс. 10 файлов)
3. Получите результат:
* До 50 участников → текстовый список
* От 51 участника → Excel-файл subscribers.xlsx

## Команды
* `/start` — начало работы
* `/help` — справка

## Особенности
* Обработка в памяти (файлы не сохраняются)
* Поддержка до 10 JSON-файлов за раз
* Docker-контейнеризация
* Приватность данных

## Технологии
* Python 3.9+
* Telegram Bot API
* Docker / Docker Compose

