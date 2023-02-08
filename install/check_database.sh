#!/bin/bash
# This is only needed in case of a docker installation

pushd /var/www/openatlas || exit

create_database () {
    echo "Database does not exist"
    echo "Install necessary postgres extensions"
    psql "$DB_URL" -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS unaccent;"

    echo "Import database dumps"
    pushd /var/www/openatlas/install || exit
    cat 1_structure.sql 2_data_model.sql 3_data_web.sql  4_data_type.sql | psql "$DB_URL" -f -
    popd || exit
}

if [ "$( psql "$DB_URL" -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'" )" == '1' ]
then
    echo "Database already exists"
    if [ "$( psql "$DB_URL" -tAc "SELECT 1 FROM $POSTGRES_DB.web.settings" )" == '1' ]
    then
      echo "Database has already data"
    else
      if [ "$OVERWRITE_DATABASE" == "TRUE" ]
      then
        create_database
      else
        echo "Database is empty. Please install backup manually"
      fi
    fi
    pushd install/upgrade/ || exit
    python3 ./database_upgrade.py || exit
    popd || exit
else
  create_database
fi

popd || exit
