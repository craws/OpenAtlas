#!/bin/bash

# shellcheck disable=SC1091

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace # Uncomment this line for debugging purposes

if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root. Aborting."
    exit 1
fi


export DB_URL="postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB"
mkdir -p $1
pg_dump ${DB_URL} > $1/$(date '+%Y-%m-%d_%H%M')_export_${POSTGRES_DB}.sql

cp -r -u -v /var/www/openatlas/files/uploads/ $1
cp -r -u -v /var/www/openatlas/files/processed_images/ $1
cp -r -u -v /var/www/openatlas/files/export/ $1

chown -R www-data:www-data $1
