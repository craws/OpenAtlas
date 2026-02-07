## INFO
From 6.6.0 on the database update script can take care of database changes,
even over multiple versions. A backup is made before changes happen. You still
should read the upgrade notes about important information.

**Limitations using the database update script**
* This should only be done within the official **main** branch of OpenAtlas
* If the database owner is not called **openatlas** (default) the SQL files
  need to be updated accordingly before

**How to upgrade**

This upgrade example is written for a Linux system. First update the code base,
then run the database upgrade script, then restart Apache:

    git pull origin main
    sudo python3 install/upgrade/database_upgrade.py
    sudo service apache2 restart

### 9.1.0 to 9.2.0
No database update is required but an additional Python package is needed:

    sudo apt install python3-fiona

### 9.0.0 to 9.1.0
9.1.0.sql is needed but will be taken care of by the database upgrade script.

Node packages are updated. Please run following command in *openatlas/static/*

    cd openatlas/static
    npm install --legacy-peer-deps

### 8.15.x to 9.0.0
WARNING - this is a major release and requires software upgrades. If you are
using a Debian system upgrade it to 13 (Trixie).

Use packages from install.md after the upgrade to be sure to have the relevant
packages, for more information and instructions see
https://redmine.openatlas.eu/issues/2343.

If you upgrade a Debian system be sure to have the new postgis
packages installed (see install.md) before you upgrade database clusters.

9.0.0.sql is needed but will be taken care of by the database upgrade script.

### 8.15.0 to 8.15.1
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 8.14.0 to 8.15.0
No database update is required but additional Python packages are needed:

#### Additional package
The unidecode package is used to transliterate URLs to ASCII.
The lxml package is used for faster and better xml creation.

    sudo apt install python3-unidecode python3-lxml

python3-dicttoxml can be removed:

    sudo apt remove python3-dicttoxml

#### New export directory structure
To adapt already exported SQL file paths to the new directory structure:

    mv /var/www/openatlas/files/export/*7z /var/www/openatlas/files/export/sql/

Be aware, that the owner of the folders might not be www-data:

    cd /var/www/openatlas
    sudo chown www-data files/export/arche/ files/export/rdf/ files/export/sql/

#### Tests (Optional)
For full test coverage, copy *ARCHE_METADATA* from 
'instance/example_testing.py' to 'testing.py'.

### 8.13.0 to 8.14.0
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 8.12.x to 8.13.0
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 8.12.0 to 8.12.1
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 8.11.0 to 8.12.0

#### Database upgrade
8.12.0.sql is needed but will be taken care of by the database upgrade script.

#### Additional package
The BeautifulSoup package is now used for improved input sanitization.

    sudo apt install python3-bs4

#### Tests
If using tests, additional packages are needed because we now use pytest.

    sudo apt install python3-pytest python3-pytes-cov

### 8.10.* to 8.11.0
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 8.9.0 to 8.10.0
8.10.0.sql is needed but will be taken care of by the database upgrade script.
Additional Python packages are needed:

    sudo apt install python3-jwt python3-python-flask-jwt-extended

### 8.8.0 to 8.9.0
8.9.0.sql is needed but will be taken care of by the database upgrade script.

### 8.7.0 to 8.8.0
8.8.0.sql is needed but will be taken care of by the database upgrade script.

### 8.6.x to 8.7.0
No database update is required but an additional Python package is needed:

    sudo apt install python3-validators

**Proxy configuration**

Proxies are now configured via the PROXIES config value and can be changed
in instance/production.py e.g.

    PROXIES = {
        'http': 'http://someurl.org:8080',
        'https': 'http://someurl.org:8080'}

The former API_PROXY value isn't used anymore and can be removed.

### 8.6.0 to 8.6.1
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 8.5.0 to 8.6.0
8.6.0.sql is needed but will be taken care of by the database upgrade script.

The additional Python package xmltodict is needed:

    sudo apt install python3-xmltodict

#### New GND reference system
A new default external reference system was added: GND, together with usage
of their API to search and display information.

In case GND is already used as reference system, make sure that it is
spelled exactly "GND" before running the database update script so that the
script can use the existing one and update it automatically without losing
already made links.

### 8.4.x to 8.5.0
8.5.0.sql is needed but will be taken care of by the database upgrade script.

Please note the changes regarding making files available via the API:
https://manual.openatlas.eu/faq.html#how-to-make-files-available-for-the-public

### 8.3.0 to 8.4.0
8.4.0.sql is needed but will be taken care of by the database upgrade script.

### 8.2.x to 8.3.0
No database updates are required but new Python packages are needed:
* python3-svgwrite (#2126 Polygons for image annotations)
* python3-shapely (#1567 WKT import)
<!-- end of the list -->
    sudo apt install python3-svgwrite python3-shapely

**For developers**

To run tests, please add a new **tests** folder to your IIIF directory, e.g.:

    mkdir /var/www/iipsrv/tests

### 8.2.0 to 8.2.1
This is a fix for installation, no need to update an existing instance.
In case you want to update it anyway, a git pull and apache restart would be
sufficient.

### 8.1.x to 8.2.0
No database updates are required but new node packages are needed:

    cd openatlas/static
    npm install

### 8.0.x to 8.1.0
8.1.0.sql is needed but will be taken care of by the database upgrade script.

New node packages are needed:

    cd openatlas/static
    npm install

#### IIIF related clean up
If you followed our Debian install instruction: although it works you can
follow these instructions to avoid error and warn messages in your logs:

* Replace **Location** with **Directory** (2 times) in
**/etc/apache2/mods-available/iipsrv.conf**, see **install/iipsrv.conf** for an
updated example
* Disable systemd to try starting the IIPImage server because it's already
started via Apache
<!-- end of the list -->
    sudo systemctl disable iipsrv.service

### 7.17.x to 8.0.0
This is a major upgrade which utilizes newer versions of underlying software.
Please consult the install.md about installation. In case you are using a
Debian system, feel free to use our own upgrade notes from the issue
description: https://redmine.openatlas.eu/issues/2038, which is already
tested.

8.0.0.sql is needed but will be taken care of by the database upgrade script.

#### Breaking changes
**Removal of frontend content management**

Because the new presentation site functionality doesn't require content
management in the backend anymore, this functionality was removed.
In case older frontend versions are still in use they would have to be
switched to the new one (OpenAtlas Discovery) or manually adapted.

**New stable API version 0.4**

The current stable API version is **0.4**. Support for API versions **0.3**
is dropped with this release including the frontend content queries mentioned
above.
