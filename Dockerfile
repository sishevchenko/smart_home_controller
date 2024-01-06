FROM python:3.11

RUN mkdir /smart_home_controller

WORKDIR /smart_home_controller

COPY /requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
