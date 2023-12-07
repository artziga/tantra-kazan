FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

#RUN pip install --upgrade pip
# Установка poetry
RUN python -m pip install --no-cache-dir poetry

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    build-essential \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/tantrakazan

WORKDIR /home

# Копирование файлов с зависимостями
COPY ./pyproject.toml .
COPY ./poetry.lock .

# Установка зависимостей
RUN poetry install

COPY ./tantrakazan ./tantrakazan