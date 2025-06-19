FROM python:latest

WORKDIR /app

COPY src .

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]
