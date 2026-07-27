#!/bin/bash
# Container entrypoint — handles both normal startup and one-shot DB initialization ("initdb" mode)

# shellcheck disable=SC1091

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace # Uncomment this line for debugging purposes

export DB_URL="postgres://openatlas:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB"

# initdb mode: initialize DB if needed, then exit
# if there is a database: do nothing
# if there is no database but a dump: import dump (don't stop on error because postgis already ships with some tables)
# if there is neither a database nor a dump, create a new db from the scripts in ./install
if [ "${1:-}" = "initdb" ]; then
  echo "Initdb mode: waiting for database..."
  until psql "$DB_URL" -tAc "SELECT 1" >/dev/null 2>&1; do 
    sleep 1
  done
  echo "Database reachable."

  has_data="$(psql "$DB_URL" -tAc "SELECT 1 FROM web.settings WHERE id = 1" || true)"
  if [ "$has_data" = "1" ]; then
    echo "Database already initialized. Nothing to do."
    exit 0
  fi

  DUMP="/var/www/openatlas/files/dump.sql"
  if [ -s "$DUMP" ]; then
    echo "Dump found at $DUMP. Importing..."
    psql "$DB_URL" -v ON_ERROR_STOP=0 -f "$DUMP"
  else
    echo "No dump found. Initializing from 0..4 SQL files."
    cd /var/www/openatlas/install
    for f in 0_extensions.sql 1_structure.sql 2_data_model.sql 3_data_web.sql 4_data_type.sql; do
      [ -f "$f" ] || { echo "Missing $f"; exit 1; }
      echo "Running $f ..."
      psql "$DB_URL" -v ON_ERROR_STOP=1 -f "$f"
    done
  fi

  has_data_post="$(psql "$DB_URL" -tAc "SELECT 1 FROM web.settings WHERE id = 1" || true)"
  if [ "$has_data_post" = "1" ]; then
    echo "Initialization verified."
    exit 0
  else
    echo "Initialization failed (marker not found in web.settings)."
    exit 1
  fi
fi

source /etc/apache2/envvars

cookie_key=$(python3 -c 'import secrets, string; print("".join(secrets.choice(string.ascii_letters + string.digits + "_") for _ in range(32)))')
export COOKIE_KEY=${COOKIE_KEY:-$cookie_key}
export MAIL_PASSWORD=${MAIL_PASSWORD:-CHANGE ME}

cat <<EOF > /var/www/openatlas/instance/production.py
DATABASE_NAME='$POSTGRES_DB'
DATABASE_USER='openatlas'
DATABASE_HOST='$POSTGRES_HOST'
DATABASE_PORT=5432
DATABASE_PASS='$POSTGRES_PASSWORD'
MAIL_PASSWORD='$MAIL_PASSWORD'
SECRET_KEY='$COOKIE_KEY'  # Used for cookies
EOF



python3 /var/www/openatlas/install/upgrade/database_upgrade.py

echo ""
exec "$@"
