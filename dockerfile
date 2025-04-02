# syntax=docker/dockerfile:1

############################
# Stage 1: Builder
############################
FROM python:3.10-slim AS builder

# Install build dependencies and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Set Poetry version
ENV POETRY_VERSION=2.1.2

# Install Poetry using the official installer
RUN curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION

# Add Poetry to PATH (it installs to /root/.local/bin by default)
ENV PATH="/root/.local/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy dependency descriptors first for caching
COPY pyproject.toml poetry.lock ./

# Install only main dependencies without creating a virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main --no-interaction --no-ansi

# Copy the rest of the application source code
COPY . .

############################
# Stage 2: Runtime
############################
FROM python:3.10-slim AS runtime

# Install runtime dependencies (and curl to install Poetry if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the complete app (including installed dependencies) from the builder
COPY --from=builder /app /app

# Ensure your entrypoint script (e.g. dbseed.sh) is executable
RUN chmod +x /app/dbseed.sh

# Expose the desired port (adjust if your app listens on a different port)
EXPOSE 5001
RUN pip install psycopg2-binary

# Set the entrypoint script (change "dbseed.sh" if you use a different startup script)
ENTRYPOINT ["./dbseed.sh"]

# Default command (if dbseed.sh doesn't override CMD)
CMD ["poetry", "run", "python", "app.py", "--gunicorn", "--env", "prod"]
