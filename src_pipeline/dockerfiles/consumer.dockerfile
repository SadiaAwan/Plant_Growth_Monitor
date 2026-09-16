FROM python:3.13-slim

WORKDIR /app
# Copy first dependency files
COPY pyproject.toml/app/
# Copy consumer file and utils folder 
COPY consumer.py ./app/
COPY utils /app/utils

# Install uv
RUN pip install --no-cache-dir uv
# Install project depedency 
RUN uv sync --no-dev 

ENV PYTHONUNBUFFERED=1

# Start MQTT-consumer 
CMD ["uv", "run", "python", "-u", "consumer.py"]

