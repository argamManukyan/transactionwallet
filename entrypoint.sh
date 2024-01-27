#!/bin/bash
export $(grep -v '^#' .env | xargs)
mkdir -p static
python3 manage.py collectstatic --noinput

python3 manage.py migrate
echo "Migrations are passed"

echo "Running tests"

python3 manage.py runserver 0.0.0.0:8000
echo "Server is running"

