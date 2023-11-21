#!/bin/bash

# shellcheck disable=SC1091

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace # Uncomment this line for debugging purposes

export DB_URL="postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB"

pg_dump ${DB_URL} > $1/$(date '+%Y-%m-%d_%H%M')_export_${POSTGRES_DB}.sql

cp -r -u -v /var/www/openatlas/files/uploads/ $1/uploads/
cp -r -u -v /var/www/openatlas/files/processed_images/ $1/processed_images/
cp -r -u -v /var/www/openatlas/files/export/ $1/export/


