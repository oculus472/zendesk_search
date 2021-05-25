FROM python:3.10.0b1

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --dev --system

COPY . /app/