#!/bin/sh

# Ожидание запуска базы данных
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z db 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Выполнение миграций базы данных и сбор статики
python manage.py makemigrations
python manage.py migrate

# Запуск Gunicorn
python manage.py runserver 0.0.0.0:8000
