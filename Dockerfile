FROM python:3.11.2-slim-buster

# Install dependencies first
RUN apt-get update && apt-get install -y \
    gcc \
    libmagic-dev \
    file \
    curl \
    gnupg \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setup app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

COPY . .

# Install Python requirements
RUN pip install --upgrade pip \
  && pip install -r requirements/prod.txt

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
