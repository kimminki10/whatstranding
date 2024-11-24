FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app
RUN apt-get update && \
    apt-get install -y pkg-config && \
    apt-get install -y build-essential && \
    apt-get install -y default-libmysqlclient-dev
RUN pip install poetry mysqlclient
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev
COPY . .

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE}

