# Instruction for merging data of the DPP and the Ostalpen projects

## Run script after preparations below

python3.5 install/scripts/ostalpen_import/import.py

## Create Ostalpen database from original dump

### Add postgis extension to begin of Ostalpen SQL

    CREATE EXTENSION postgis;

### Search and replace following strings in Ostalpen SQL

    openatla; with openatlas;

### Create new database

    dropdb ostalpen
    createdb ostalpen -O openatlas

## Put new version online

- change settings (mail!)
- change content text

### Execute upgrades

    psql openatlas_dpp_origin < install/upgrade/3.6.0.sql
    deactivate mail in admin

### Make a new SQL dump

    pg_dump openatlas_dpp > instance/dpp_origin.sql
