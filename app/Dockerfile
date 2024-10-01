FROM python:3-bookworm

EXPOSE 80

ENV PYTHONUNBUFFERED 0

RUN pip install gunicorn

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY app.py /app.py
COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY wait_postgres.py /wait_postgres.py

ENTRYPOINT ["sh", "-c", "/docker-entrypoint.sh"]

