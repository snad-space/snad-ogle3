FROM python:3-buster

EXPOSE 80

RUN pip install gunicorn

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY app.py /app.py

ENTRYPOINT ["gunicorn", "-w4", "-b0.0.0.0:80", "app:app"]

