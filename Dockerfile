FROM python3.11-alpine

ENV PYTHONENVBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk-get update && \
    python3 -m venv venv && \
    pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]