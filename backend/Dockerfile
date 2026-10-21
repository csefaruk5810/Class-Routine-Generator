FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
RUN pip install --upgrade pip && pip install .

COPY . /app

EXPOSE 8000

