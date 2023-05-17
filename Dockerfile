# Используем базовый образ Python
FROM python:3.9

# Установка зависимостей
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода приложения
COPY . /app

# Установка переменных окружения
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE geef.settings