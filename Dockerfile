FROM python:3.11

RUN mkdir /smart_home_controller

WORKDIR /smart_home_controller

COPY /requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN alembic revision --autogenerate -m "default"

RUN alembic upgrade head

CMD uvicorn main:app --bind=0.0.0.0:8000
