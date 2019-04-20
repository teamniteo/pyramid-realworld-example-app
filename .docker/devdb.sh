#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER conduit_dev WITH PASSWORD '';
  CREATE DATABASE conduit_dev;
  GRANT ALL PRIVILEGES ON DATABASE conduit_dev TO conduit_dev;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "conduit_dev" <<-EOSQL
  CREATE EXTENSION IF NOT EXISTS pgcrypto;
  SELECT gen_random_uuid();
EOSQL
