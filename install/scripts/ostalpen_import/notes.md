# Instruction for merging data of the DPP and the Ostalpen projects

## Run script after preparations below

python3.5 install/scripts/ostalpen_import/import.py

## Create Ostalpen database from original dump

### Fetch latest dump

From cPanel: Datenbanken > PostgreSQL backups > latest openatla_main_db.sql.gz

### Search and replace following strings in Ostalpen SQL

    openatla; with openatlas;

### Create new database

    dropdb ostalpen
    createdb ostalpen -O openatlas
    psql ostalpen -c "CREATE EXTENSION postgis;"
    psql ostalpen < ~/Desktop/openatla_main_db.sql

## Put new version online

    pgdump openatlas_dpp > ~/Desktop/dpp.sql

make upgrades

    git pull github dev

upload and install db

upload images

make Stefan manager

change settings (mail!) and content text
