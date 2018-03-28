# Installation Notes

Installation with examples from a Debian 9 (Stretch) system.

## Requirements

### Python 3 and Flask

    # apt-get install python3 python3-bcrypt python3-dateutil python3-jinja2 python3-psycopg2
    # apt-get install python3-flask python3-flask-babel python3-flask-login python3-flaskext.wtf
    # apt-get install python3-markdown python3-numpy

### Apache 2.4

    # apt-get install apache2 libapache2-mod-wsgi-py3

### PostgreSQL 9.6

    # apt-get install postgresql postgresql-9.6-postgis-2.3 postgresql-9.6-postgis-2.3-scripts

### gettext

    # apt-get install gettext

## Installation

## Database

Important!

A user with username "OpenAtlas" and password "change_me_PLEASE!" is created.
Change this account immediately!

As postgres

    $ createuser openatlas -P
    $ createdb openatlas -O openatlas

Uncomment "CREATE EXTENSION postgis;" in top off install/structure.sql

    $ cd install
    $ cat structure.sql data_web.sql data_model.sql data_node.sql | psql -d openatlas -f -

### Files

Copy the files to /var/www/your_sitename

## Configuration

Copy instance/example_production.py to instance/production.py and add/change values as appropriate.

    $ cp  instance/example_production.py instance/production.py

## Apache

As root copy and adapt install/example_apache.conf for a new vhost, activate the site:

    # a2ensite your_sitename

Test Apache configuration and restart

    # apache2ctl configtest
    # service apache2 restart

## File Upload

Make the openatlas/uploads directory writeable for apache e.g.

    chown www-data /var/www/net/openatlas/openatlas/uploads/

## Finishing

Login with username "OpenAtlas" and password "change_me_PLEASE!" and change the password in profile.
Remove the data/install directory on production systems

## Unit tests (optional)

Install required packages:    
    
    # apt-get install python3-coverage python3-nose
    
As postgres

    $ createdb openatlas_test -O openatlas
    
Uncomment "CREATE EXTENSION postgis;" in top off install/structure.sql

    $ cd install    
    $ cat structure.sql data_web.sql data_model.sql | psql -d openatlas_test -f -

Comment "CREATE EXTENSION postgis;" again before running tests.

Use these parameters for running with coverage and HTML report:

    --with-coverage --cover-package openatlas --cover-html --cover-tests --cover-erase   


