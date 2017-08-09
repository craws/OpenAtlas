# Important Notice

This is the Python/Flask port of OpenAtlas. It is still in development and not for productive use. Use at own risk!

# Installation Notes

Installation with examples from a Debian 9 (Stretch) system.

## Requirements

### Python 3 and Flask

    # apt-get install python3 python3-bcrypt python3-dateutil python3-jinja2 python3-psycopg2 python3-markdown
    # apt-get install python3-flask python3-flask-babel python3-flask-login python3-flaskext.wtf

### Apache 2.4

    # apt-get install apache2 libapache2-mod-python libapache2-mod-wsgi-py3

### PostgreSQL 9.6

    # apt-get install python3-coverage python3-nose

### gettext

    # apt-get install gettext

## Installation

## Database



As postgres

    $ createuser openatlas -P
    $ createdb openatlas -O openatlas

    Uncomment "CREATE EXTENSION postgis;" in top off install/structure.sql

    $ cd install
    $ cat structure.sql data_web.sql data_model.sql | psql -d openatlas -f -

Optional: create database openatlas_test for tests

### Files

Copy the files to /var/www/your_sitename

Create the folder /var/www/your_sitename/instance

## Configuration

Copy install/instance_config.py instance/config.py

Change the values in instance/config.py as appropriate

## Apache

use install/apache_example.conf as template for a new vhost

    # a2ensite your_sitename
    # apacha2ctl configtest
    # service apache2 restart

## Python packages to run tests

    # apt-get install python3-coverage python3-nose

## Finishing

Remove the data/install directory on production systems




