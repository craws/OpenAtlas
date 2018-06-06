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

### Files

Copy the files to /var/www/your_sitename or clone it from Bitbucket

### Database

Important!
A user with username "OpenAtlas" and password "change_me_PLEASE!" is created.
Change this account immediately!

As postgres

    $ createuser openatlas -P
    $ createdb openatlas -O openatlas
    $ psql openatlas -c "CREATE EXTENSION postgis;"
    $ cd install
    $ cat structure.sql data_web.sql data_model.sql data_node.sql | psql -d openatlas -f -

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

### File Upload

Make the openatlas/uploads directory writeable for apache e.g.

    # chown www-data openatlas/uploads

### Finishing

Login with username "OpenAtlas" and password "change_me_PLEASE!" and change the password in profile.

### Unit tests (optional)

Install required packages:

    # apt-get install python3-coverage python3-nose

As postgres

    $ createdb openatlas_test -O openatlas
    $ psql openatlas_test -c "CREATE EXTENSION postgis;"
    $ cd install
    $ cat structure.sql data_web.sql data_model.sql | psql -d openatlas_test -f -

Comment "CREATE EXTENSION postgis;" again before running tests.

Copy instance/example_testing.py to instance/testing.py

    $ cp instance/example_testing.py instance/testing.py

Add/change values as appropriate.

Use these parameters for running with coverage and HTML report:

    --with-coverage --cover-package openatlas --cover-html --cover-tests --cover-erase
