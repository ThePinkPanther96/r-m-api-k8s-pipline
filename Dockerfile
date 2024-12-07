FROM python:3

MAINTAINER Gal

WORKDIR /app

COPY app /app

COPY app/requirements.txt ./

RUN pip install --upgrade pip

RUN echo ${BUILD_NUMBER} && pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

ARG BUILD_NUMBER

ENV ENVIRONMENT=DEV

ENTRYPOINT ["python", "rick_and_morty.py"]