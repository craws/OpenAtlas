#!/bin/bash
# This is only needed in case of a docker installation

# shellcheck disable=SC1091

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace # Uncomment this line for debugging purposes

# THIS SCRIPT IS NOT IN USE

export DB_URL="postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB"

if [ "$( psql "$DB_URL" -tAc "SELECT 1 FROM web.settings WHERE id = 1" )" == $'1' ]
  then
    echo 'Database has already data'
  else
    echo $'Database has no data'
    cd /var/www/openatlas/install && cat [0-9]_*.sql
    psql "$DB_URL" -f -
fi

echo ""
exec "$@"
