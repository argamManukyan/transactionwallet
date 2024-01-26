FROM python:3.11-alpine

ENV PYTHONENVBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN apk  update && \
    pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

RUN ["chmod", "+x", "entrypoint.sh"]
CMD ["sh","entrypoint.sh"]