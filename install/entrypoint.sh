#!/bin/bash

# shellcheck disable=SC1091

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace # Uncomment this line for debugging purposes

export DB_URL="postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB"
psql $DB_URL -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS unaccent;"
pushd /var/www/openatlas/install
cat 1_structure.sql 2_data_model.sql 3_data_web.sql 4_data_type.sql | psql $DB_URL -f -
popd

source /etc/apache2/envvars

cookie_key=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c 32;echo;)
export COOKIE_KEY=${COOKIE_KEY:-$cookie_key}
export MAIL_PASSWORD=${MAIL_PASSWORD:-CHANGE ME}

cat <<EOF > /var/www/openatlas/instance/production.py
DATABASE_NAME='$POSTGRES_DB'
DATABASE_USER='$POSTGRES_USER'
DATABASE_HOST='$POSTGRES_HOST'
DATABASE_PORT=5432
DATABASE_PASS='$POSTGRES_PASSWORD'
MAIL_PASSWORD='$MAIL_PASSWORD'
SECRET_KEY='$COOKIE_KEY'  # Used for cookies
EOF

echo ""
exec "$@"