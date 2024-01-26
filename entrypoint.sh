#!/bin/bash
mkdir -p static
python3 manage.py collectstatic --noinput
python3 manage.py migrate
echo "Migrations are passed"

python3 manage.py runserver 0.0.0.0:8000
echo "Server is running"

