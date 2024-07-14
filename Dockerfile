FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
