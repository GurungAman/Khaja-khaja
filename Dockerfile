FROM python:3.8.5

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app/khaja_khaja
COPY requirements-dev.txt /usr/src/app/khaja_khaja
RUN pip install --upgrade pip \
    && pip install -r requirements-dev.txt

COPY . /usr/src/app