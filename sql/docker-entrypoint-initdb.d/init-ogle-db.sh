#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ogle WITH PASSWORD 'ogle';
    CREATE USER app;
    CREATE DATABASE ogle;
    GRANT ALL PRIVILEGES ON DATABASE ogle TO ogle;
    GRANT CONNECT ON DATABASE ogle TO app;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname ogle <<-EOSQL
    CREATE EXTENSION pg_sphere;
EOSQL

bzcat /ogle.sql.bz2 | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname ogle

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname ogle <<-EOSQL
    VACUUM FULL ANALYZE;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname ogle <<-EOSQL
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO app;
    REVOKE CREATE ON SCHEMA public FROM public;
EOSQL
