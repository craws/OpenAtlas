# Instruction for merging data of the DPP and the Ostalpen projects

## Run script after preparations below

python3 install/ostalpen/import.py

## Create Ostalpen database from original dump

### Add postgis extension to begin of Ostalpen SQL

    CREATE EXTENSION postgis;

### Search and replace following strings in Ostalpen SQL

    openatla; with openaltas;

### Create new database

    dropdb ostalpen
    createdb ostalpen -O openatlas

## Put new version online

- change settings (mail!)
- change content text

## Create new current DPP database

### Created new database

    dropdb openatlas_dpp_origin
    createdb openatlas_dpp_origin -O openatlas
    psql openatlas_dpp_origin < dpp.sql

### Execute upgrades

    psql openatlas_dpp_origin < install/upgrade/3.6.0.sql
    deactivate mail in admin

### Make a new SQL dump

    pg_dump openatlas_dpp_origin > instance/dpp_origin.sql
