FROM python:3.13-slim

WORKDIR / app

# Installer uv
RUN pip install --no-cache-dir uv

# Kopiera först beroendefilerna
COPY pyproject.toml uv.lock ./

# Installera projektets dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Kopiera consumer-programmer och utils-mappen
COPY consumer.py ./
COPY utils ./utils

# Starta MQTT-consumern
CMD ["uv", "run", "--no-sync", "python", "consumer.py"]

