FROM python:3.11-slim

# Add Debian repositories and install libmagic dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libmagic-dev \
    file \
    && rm -rf /var/lib/apt/lists/*

# Set up app
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements/prod.txt

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
