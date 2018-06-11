FROM python:3.6-slim

SHELL ["/bin/bash", "-c"]

# Just disables the tensorflow warning, doesn't enable AVX/FMA
ENV TF_CPP_MIN_LOG_LEVEL=2

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    openssh-client \
    graphviz-dev \
    pkg-config \
    git-core \
    openssl \
    libssl-dev \
    libffi6 \
    libffi-dev \
    libpng-dev \
    curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Copy as early as possible so we can cache ...
ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . /app

VOLUME ["/app/data", "/app/actions", "/app/model", "/app/logs"]

EXPOSE 5005