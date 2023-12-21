FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCKER_RUN=True

# Update files
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    libxslt-dev \
    libpq-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    gettext \
    cron \
    openssh-client \
    flake8 \
    locales \
    vim \
    wait-for-it

# Install Python development packages
RUN apt-get install -y \
    python3-dev

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password --gecos ""  rootuser

COPY ./src /src
WORKDIR /src

RUN chown -R rootuser:rootuser .

USER rootuser

CMD gunicorn -w 1 --chdir ./src config.asgi:application --bind 0.0.0.0:8000 --forwarded-allow-ips="*.*"
