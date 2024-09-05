FROM python:3.11-slim

EXPOSE 8000

WORKDIR /api

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

RUN chmod +x ./wait-for-it.sh

ENTRYPOINT ["/bin/bash", "-c", "./wait-for-it.sh postgres:5432 --timeout=60 -- python manage.py migrate && python manage.py seed_db && python manage.py runserver 0.0.0.0:8000"]