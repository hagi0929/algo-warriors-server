#!/bin/sh
set -e

# Source environment variables from .env if available
if [ -f /app/.env ]; then
  . /app/.env
fi

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT} to be ready..."
# Simple wait; consider a loop or wait-for-it.sh for production
sleep 5


if [ "$SEED_DB" = "true" ]; then
  echo "Seeding the database..."
  echo "Creating tables..."
  PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_DATABASE" -f /app/setup/create_table/create_table.sql

  echo "Creating indexes..."
  PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_DATABASE" -f /app/setup/create_table/create_index.sql

  echo "Populating user data..."
  poetry run python /app/setup/populate_table/populate_user.py

  echo "Populating main table data..."
  poetry run python /app/setup/populate_table/populate_table.py

  echo "Populating discussions..."
  poetry run python /app/setup/populate_table/populate_discussions.py

  echo "Populating tag table..."
  poetry run python /app/setup/populate_table/populate_tag_table.py
else
  echo "Skipping seeding step as SEED_DB is not set to 'true'."
fi

