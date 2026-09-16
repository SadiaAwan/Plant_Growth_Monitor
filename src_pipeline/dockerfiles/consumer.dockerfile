FROM python:3.13-slim

WORKDIR /app
# Copy first dependency files
COPY pyproject.toml uv.lock ./
# Copy consumer file and utils folder 
COPY consumer.py ./
COPY utils ./utils

# Install uv
RUN pip install --no-cache-dir uv
# Install project depedency 
RUN uv sync --frozen --no-dev --no-install-project

ENV PYTHONUNBUFFERED=1

# Start MQTT-consumer 
CMD ["uv", "run", "python", "-u", "consumer.py"]

