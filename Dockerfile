FROM python:3.13.7-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
