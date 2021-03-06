FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/djangoProject_delivery_rest

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/djangoProject_delivery_rest
COPY ./prestart.sh /usr/src/prestart.sh

EXPOSE 8000