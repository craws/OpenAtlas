# Important Notice

This is the Python/Flask port of OpenAtlas. It is still in development and not for productive use. Use at own risk!

# Installation Notes

Installation with examples from a Debian 8.3 (Jessie) system.

There is a good chance that we switch to Debian (Stretch) and Python 3 before releasing 1.0.0

## Requirements

### Python 2

    # apt-get install python python-flask python-flask-babel python-flask-login python-flaskext.wtf python-jinja2

### Apache 2.4

    # apt-get install apache2 libapache2-mod-passenger libapache2-mod-python libapache2-mod-wsgi

### PostgreSQL 9.5

    # apt-get install postgis postgresql-9.5-postgis-2.1

### gettext

    # apt-get install gettext

## Installation

## Database

As postgres

    $ createuser openatlas -P
    $ createdb openatlas -O openatlas
    $ cd data/install
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

## Finishing

Remove the data/install directory on production systems




