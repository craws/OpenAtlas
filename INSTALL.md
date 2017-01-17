# Installation Notes

Installation with examples from a Debian 8.3 (Jessie) system.

## Requirements

### Apache 2.4

    # apt-get install apache2 libapache2-mod-python libapache2-mod-wsgi

### Python 2.7 and Flask

    # apt-get install python2.7 python-flask python-flask-babel python-flask-login python-flaskext.wtf python-psycopg2

### PostgreSQL 9.5

add postgresql server to /etc/apt/sources.list:
deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main

    # apt-get install postgresql postgis postgresql-9.5-postgis-2.1

### gettext

    # apt-get install gettext

## Installation

### Files

copy the files to /var/www/your_sitename

### Database

WARNING! After importing data_web.sql you can login as admin (username: a, password: a), change this account immediately!

PostGis is needed. To add it uncomment "CREATE EXTENSION postgis;" on top of data/install/structure.sql

as postgres

    $ createuser openatlas_master -P
    $ createdb openatlas_master -O openatlas_master
    $ cd data/install
    $ cat structure.sql data_web.sql data_model.sql data_node.sql | psql -d openatlas_master -f -

optional - create database openatlas_master_test for unittests

### Configuration

adapt /application/configs/config.ini

adapt and rename /application/configs/password_example.ini to password.ini

### Apache

use apache_example.conf as template for a new vhost

    # a2ensite your_sitename
    # apacha2ctl configtest
    # /etc/init.d/apache2 restart

### Finishing

- change default user and password
- remove the data/install directory
