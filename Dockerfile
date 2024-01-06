FROM python:3.11

RUN mkdir /currency_convertor

WORKDIR /currency_convertor

COPY requirements/prod.txt .

RUN pip install -r prod.txt

COPY . .

CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bild=0.0.0.0:8000