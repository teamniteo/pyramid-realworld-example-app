#!/usr/bin/env nix-shell
#!nix-shell --argstr type run -i bash /app/shell.nix

set -e

echo "Running database migrations"
alembic -c etc/alembic.ini -x ini=etc/production.ini upgrade head || echo "Database migrations failed!"
echo "Done"
