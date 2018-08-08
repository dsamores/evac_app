FROM python:3.6

RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        postgresql-client

# ENV PYTHONUNBUFFERED 1
# ENV DJANGO_ENV staging

COPY ./requirements.txt /code/requirements.txt
RUN pip install -Ur /code/requirements.txt
# ARG IS_LOCAL_ENV

COPY . /code/
WORKDIR /code/

COPY /scripts/entrypoint.sh /entrypoint.sh
ENTRYPOINT /entrypoint.sh
