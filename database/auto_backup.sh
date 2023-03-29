#!/bin/sh
if test ! -f "/bin/pg_dump"; then
    echo "Postgres not installed, skipping backup"
    exit 0
else
    echo "Creating backup with pg_dump"
    pg_dump -U postgres -d anime_suggester -h localhost -p 5432 -Fc -f /var/lib/postgresql/backup/backup_$(date +%Y-%m-%d_%H-%M-%S).sql
fi