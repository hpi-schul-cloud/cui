FROM python:3.6-slim

SHELL ["/bin/bash", "-c"]

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    build-essential \
    git-core \
    openssl \
    libssl-dev \
    libffi6 \
    libffi-dev \
    curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Copy as early as possible so we can cache ...
ADD requirements.txt .

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_md \
    && python -m spacy link en_core_web_md en

ADD . /app

VOLUME ["/app/projects", "/app/data", "/app/config.yml"]

EXPOSE 5000