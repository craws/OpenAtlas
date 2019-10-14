# Installation Notes

Some knowledge about package installation, web server and database configuration will be needed.

This software was developed and tested on Linux/Debian 10 (codename "buster") and the easiest way to
install would be on Debian 10 system following these instructions.

It may work on other Linux distributions or even on non Linux systems but would need substantially
more knowledge about server administration.

## Requirements

### Python 3.7 and Flask 1.0

    # apt-get install python3 python3-bcrypt python3-dateutil python3-jinja2 python3-psycopg2
    # apt-get install python3-flask python3-flask-babel python3-flask-login python3-flaskext.wtf
    # apt-get install python3-markdown python3-numpy python3-pandas python3-fuzzywuzzy

### Apache 2.4

    # apt-get install apache2 libapache2-mod-wsgi-py3

### PostgreSQL 11 and PostGIS 2.5

    # apt-get install postgresql postgresql-11-postgis-2.5 postgresql-11-postgis-2.5-scripts

### gettext

    # apt-get install gettext

## Installation

### Files

Copy the files to /var/www/your_site_name or clone OpenAtlas from GitHub

    $ git clone https://github.com/craws/OpenAtlas.git

### Database

The commands below have to be executed as postgres.

Create an openatlas database user

    $ createuser openatlas -P

Create an openatlas database, make openatlas the owner of it

    $ createdb openatlas -O openatlas

Add the postgis extension to the database

    $ psql openatlas -c "CREATE EXTENSION postgis;"

Import the scripts: 1_structure.sql,  2_data_web.sql,  3_data_model.sql, 4_data_node.sql

    $ cd install
    $ cat 1_structure.sql 2_data_web.sql 3_data_model.sql 4_data_node.sql | psql -d openatlas -f -

**Important!** A user with user name "OpenAtlas" and password "change_me_PLEASE!" is created.

**Change this account immediately!**

### Configuration

Copy instance/example_production.py to instance/production.py

    $ cp instance/example_production.py instance/production.py

Add/change values as appropriate. See config/default.py which settings are available.

### Apache

As root copy and adapt install/example_apache.conf for a new vhost, activate the site:

    # a2ensite your_sitename

Test Apache configuration and restart

    # apache2ctl configtest
    # service apache2 restart

### File Upload and Export

Make these directories writeable for the Apache user:

openatlas/uploads

openatlas/export/csv

openatlas/export/sql

e.g.

    # chown www-data openatlas/uploads

### Finishing

Login with username "OpenAtlas" and password "change_me_PLEASE!" and change the password in profile.

### Upgrade

If you later like to upgrade the application be sure to read and follow the [upgrade instructions](install/upgrade/upgrade.md).

### Additional security (optional)

You don't need this to run the application but it will improve server side security if running an online productive instance.

Use certbot to create a https vhost.

When configured Apache to use HTTPS only, add this line to instance/production.py:

    SESSION_COOKIE_SECURE = True

### Unit tests (optional)

Install required packages:

    # apt-get install python3-coverage python3-nose

As postgres

    $ createdb openatlas_test -O openatlas
    $ psql openatlas_test -c "CREATE EXTENSION postgis;"
    $ cd install
    $ cat 1_structure.sql 2_data_web.sql 3_data_model.sql 4_data_node.sql | psql -d openatlas_test -f -

Copy instance/example_testing.py to instance/testing.py

    $ cp instance/example_testing.py instance/testing.py

Add/change values as appropriate.

Use these parameters for running with coverage and HTML report:

    --with-coverage --cover-package openatlas --cover-html --cover-tests --cover-erase
