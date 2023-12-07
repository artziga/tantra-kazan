FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    cmake \
    make \
    g++ \
    zlib-dev \
    libjpeg \
    libjpeg-turbo-dev \
    libpng-dev \
    libwebp-dev \
    tiff-dev \
    openblas \
    openblas-dev \
    freetype-dev \
    libffi-dev \
    openssl-dev \
    gdal \
    gdal-dev  \

RUN pip install --upgrade pip

RUN mkdir -p /home/tantrakazan

WORKDIR /home

# Копирование файлов с зависимостями
COPY ./requirements.txt /home/tantrakazan

# Установка зависимостей
RUN pip install -r /home/tantrakazan/requirements.txt

COPY . /home/tantrakazan

RUN pip install --upgrade pip

RUN mkdir -p /home/tantrakazan

WORKDIR /tantrakazan

# Копирование файлов с зависимостями
COPY ./requirements.txt /tantrakazan

# Установка зависимостей
RUN pip install -r /tantrakazan/requirements.txt

COPY . /tantrakazan
EXPOSE 8000
CMD ["python", "manage.py", "runserver 0.0.0.0:8000"]