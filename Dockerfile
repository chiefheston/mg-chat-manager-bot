FROM python:3.14.1-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python3-dev \

COPY ../pyproject.toml /app
COPY ../uv.lock /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir uv

RUN uv sync --frozen

WORKDIR /app/src
COPY src .

CMD ["uv", "run", "src/main.py"]