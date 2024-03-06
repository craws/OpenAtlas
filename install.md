# Installation Notes
Some knowledge about package installation, web server and database
configuration will be needed.

This software was developed and tested on Linux/Debian 12.2
(codename "bookwom") and the easiest way to install would be on a
[Debian](https://www.debian.org/) 12.2 system following these instructions.

Another (experimental) way to install it would be via
[Docker](https://www.docker.com/).
For more information take a look at the end of this document.

It may also work on other Linux distributions or even non Linux systems with
using the [requirements.txt](requirements.txt), but substantially more
knowledge about server administration would be needed.

Feel free to also consult our own
[documentation](https://redmine.openatlas.eu/projects/uni/wiki/Debian_server_installation)
that we are using to set up Debian servers for OpenAtlas installations.

* [Requirements](#Requirements)
* [IIIF](#IIIF) (optional)
* [Tests](#Tests) (optional)
* [Docker](#Docker) (alternative installation method)

## Requirements
### Python 3.11 and Flask 2.2.2
    sudo apt install python3 python3-bcrypt python3-dateutil python3-psycopg2 python3-fuzzywuzzy python3-flask
    sudo apt install python3-flask-babel python3-flask-login python3-flaskext.wtf python3-markdown python3-numpy
    sudo apt install python3-pandas python3-jinja2 python3-flask-cors python3-flask-restful p7zip-full
    sudo apt install python3-wand python3-rdflib python3-dicttoxml python3-rdflib-jsonld python3-flasgger
    sudo apt install python3-requests exiftran python3-email-validator python3-svgwrite

### Apache 2.4
    sudo apt install apache2 libapache2-mod-wsgi-py3

### PostgreSQL 15 and PostGIS 3
    sudo apt install postgresql postgresql-15-postgis-3 postgresql-15-postgis-3-scripts

### gettext, pip, npm
    sudo apt install gettext npm

## Installation
### Files
Copy the files to /var/www/your_site_name or clone OpenAtlas from GitHub and
adapt them accordingly as regular user:

    git clone https://github.com/craws/OpenAtlas.git

### Frontend libraries
Execute this lines as regular user too:

    cd openatlas/static
    npm install

### Database
Executed statements below as **postgres** user.

Create an openatlas database user

    createuser openatlas -P

Create an openatlas database, make openatlas the owner of it

    createdb openatlas -O openatlas

Add the [PostGIS](https://postgis.net/) and unaccent extension to the database

    psql openatlas -c "CREATE EXTENSION postgis; CREATE EXTENSION unaccent;"

Import the SQL files:

    cd install
    cat 1_structure.sql 2_data_model.sql 3_data_web.sql 4_data_type.sql | psql -d openatlas -f -

A user with username **OpenAtlas** is created with the password
**change_me_PLEASE!**

**Important**: change this account immediately. A warning will be displayed for
admins until this account is changed.

### Configuration
Copy instance/example_production.py to instance/production.py

    cp instance/example_production.py instance/production.py

Add/change values as appropriate. See config.py which settings are available.

### Apache
As root copy and adapt install/example_apache.conf for a new vhost, activate
the site:

    sudo a2ensite your_sitename

Test Apache configuration and restart

    sudo apache2ctl configtest
    sudo service apache2 restart

Make the **files** directory writable for the Apache user, e.g.:

    sudo chown -R www-data files

### Finishing
Login with username "OpenAtlas" and password "change_me_PLEASE!" and change the
password in profile. You may want to check the admin area to set up default
site settings, email and similar.

### Upgrade
If you later like to upgrade the application be sure to read and follow the
[upgrade instructions](install/upgrade/upgrade.md).

### Additional security (optional)
You don't need this to run the application, but it will improve server side
security if running an online productive instance.

Use certbot to create a https vhost.

After Apache is configured to use HTTPS only, add this line to
instance/production.py:

    SESSION_COOKIE_SECURE = True

## IIIF

[IIIF](https://iiif.io/) is a set of open standards for delivering
high-quality, attributed digital objects online at scale. Be aware that:

* IIIF is **optional** for an OpenAtlas installation
* Although already working and in use we still consider it **experimental**
* Enabling IIIF can expose files to the public (without login)

### Installation

    sudo apt install iipimage-server libvips-tools
    sudo a2enmod fcgid
    sudo service apache2 restart

You can test http://your.server/iipsrv/iipsrv.fcgi to see if it runs.

    sudo mkdir /var/www/iipsrv
    sudo cp -p /usr/lib/iipimage-server/iipsrv.fcgi /var/www/iipsrv/
    sudo chown -R www-data /var/www/iipsrv

### Configuration

Edit the configuration to your needs, see example at
[install/iipsrv.conf](install/iipsrv.conf) and restart Apache:

    sudo vim /etc/apache2/mods-available/iipsrv.conf
    sudo service apache2 restart

If using Debian, prevent systemd to try to start the service itself:

    sudo systemctl disable iipsrv.service

Further configuration can be done at the IIIF tab in the admin area of the web
application.

## Tests
Install required packages:

    sudo apt install python3-coverage python3-nose

As postgres:

    createdb openatlas_test -O openatlas
    psql openatlas_test -c "CREATE EXTENSION postgis; CREATE EXTENSION unaccent;"

Copy instance/example_testing.py to instance/testing.py and adapt as needed:

    cp instance/example_testing.py instance/testing.py

Run tests

    nosetest3

Run tests with coverage

    nosetests3 -c tests/.noserc

## Docker
Be aware, the [Docker](https://www.docker.com/) installation is experimental
and is **not** recommended for usage on a productive system.

To run OpenAtlas as a Docker container clone the repository

    git clone https://github.com/craws/OpenAtlas.git

Open an CLI in the directory where you cloned OpenAtlas and run

    docker compose up --detach

After the containers are build an OpenAtlas instance is available under
**localhost:8080**.

Login with username **OpenAtlas** and password **change_me_PLEASE!** and change
the password in your profile. You may want to check the admin area to set up
default site settings, email and similar.

### Restore database dump
To restore a database SQL dump uncomment following command in
./docker-compose.yml and modify the first path. Make sure that no previous
database is installed (e.g. delete ./data/db/), as the dump will not be
executed.

    - ./files/export/dump.sql:/docker-entrypoint-initdb.d/dump.sql
