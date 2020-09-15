FROM python:3.8-alpine as poetry 
WORKDIR /requirements/
RUN apk \
add \
gcc \
libffi-dev \
musl-dev \
openssl-dev 
#postgresql-dev \
#python3-dev && \
#pip install poetry
COPY pyproject.toml poetry.lock /
RUN pip install poetry && \
poetry export -f requirements.txt -o /requirements/base.txt && \
poetry export --dev -f requirements.txt -o /requirements/dev.txt

FROM python:3.8-alpine
RUN apk \
add \
gcc \
musl-dev \
postgresql-dev

WORKDIR /app
COPY --from=0 /requirements .
RUN pip install -r base.txt

COPY . /app
