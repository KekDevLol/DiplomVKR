# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1 # Не создавать .pyc файлы
ENV PYTHONUNBUFFERED 1        # Выводить логи сразу, без буферизации

COPY Pipfile .
RUN python -m pip install --upgrade pip \
    && pip install --no-compile --progress-bar=off pipenv \
    && pipenv lock --dev --clear \
    && pipenv --clear install --system --dev \
    && pipenv install "setuptools==71.1.0"


# Копируем файлы зависимостей
COPY Pipfile Pipfile.lock ./

# Устанавливаем зависимости проекта
RUN pipenv install --system --deploy

# Копируем исходный код проекта в рабочую директорию
COPY ./src ./src

# Команда по умолчанию
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]