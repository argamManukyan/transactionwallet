FROM python3.11-alpine

ENV PYTHONENVBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk-get update

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]