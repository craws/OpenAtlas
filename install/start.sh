#!/bin/bash

pushd /var/www/openatlas || exit

if [ "$( psql $DB_URL -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'" )" = '1' ]
then
    echo "Database already exists"
    if [ "$( psql $DB_URL -tAc "SELECT 1 FROM $POSTGRES_DB.web.settings" )" = '1' ]
    then
      echo "Database has already data"
    else
      echo "Database is empty. Please install backup manually"
    fi
    pushd install/upgrade/ || exit
    python3 database_upgrade.py || exit
    popd || exit
else
    echo "Database does not exist"
    echo "Install necessary postgres extensions"
    psql $DB_URL -c "CREATE EXTENSION postgis; CREATE EXTENSION unaccent;"

    echo "Import database dumps"
    pushd /var/www/openatlas/install || exit
    cat 1_structure.sql 2_data_model.sql 3_data_web.sql  4_data_node.sql | psql $DB_URL -f -
    popd || exit
fi
popd || exit