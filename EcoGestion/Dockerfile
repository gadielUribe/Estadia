FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        default-mysql-client \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Wrapper que fuerza --ssl-mode=DISABLED para cualquier invocación a mysqldump
RUN printf '#!/bin/sh\nexec /usr/bin/mysqldump --skip-ssl "$@"\n' > /usr/local/bin/mysqldump \
 && chmod +x /usr/local/bin/mysqldump

# Wrapper para 'mysql' (restauración): desactiva SSL por default
RUN printf '#!/bin/sh\nexec /usr/bin/mysql --skip-ssl "$@"\n' > /usr/local/bin/mysql \
 && chmod +x /usr/local/bin/mysql


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]