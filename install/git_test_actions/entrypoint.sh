#!/bin/bash

# shellcheck disable=SC1091

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace # Uncomment this line for debugging purposes

export DB_URL="postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB"
psql $DB_URL -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS unaccent;"

cat <<EOF > /var/www/openatlas/instance/testing.py
DATABASE_NAME='$POSTGRES_DB'
DATABASE_USER='$POSTGRES_USER'
DATABASE_HOST='$POSTGRES_HOST'
DATABASE_PORT=5432
DATABASE_PASS='$POSTGRES_PASSWORD'
MAIL_PASSWORD='$MAIL_PASSWORD'
SECRET_KEY='$COOKIE_KEY'  # Used for cookies
IS_UNIT_TEST = True
DEBUG = True
EOF

echo ""
exec "$@"