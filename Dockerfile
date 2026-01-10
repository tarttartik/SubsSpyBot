# 1. Базовый образ
FROM python:3.11-slim

# 2. Системные зависимости (если потребуется gcc для каких-то пакетов)
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# 3. Рабочая директория
WORKDIR /app

# 4. Копируем файл зависимостей и ставим пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь проект
COPY . .

# 6. Непривилегированный пользователь
RUN addgroup --gid 1001 --system bot && \
    adduser  --uid 1001 --system --ingroup bot bot && \
    chown -R bot:bot /app
USER bot

# 7. Запуск
CMD ["python", "-m", "src.bot.main"]