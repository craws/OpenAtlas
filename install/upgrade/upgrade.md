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

**Multiple instances**

When using the multiple instances approach be aware about slightly changes at
the upgrade process. E.g. you only need to update the application once but
have to do the database upgrade for every instance individually by going in
their specific directories and execute:

    sudo python3 database_upgrade.py

### 9.3.x to 9.4.0
9.4.0.sql is needed but will be taken care of by the database upgrade script.

New NPM packages with security updates are available:

    cd openatlas/static
    npm install

### 9.2.0 to 9.3.0
9.3.0.sql is needed but will be taken care of by the database upgrade script.

Additional Python packages are needed:

    sudo apt install python3-flask-bcrypt python3-magic python3-levenshtein

One Python library is not needed by OpenAtlas anymore and may be removed:

    apt purge python3-fuzzywuzzy

Node packages are updated. Please run following command in
**openatlas/static/**

    cd openatlas/static
    npm install

SESSION_COOKIE_SECURE in config/default.py now defaults to **True**.
In case OpenAtlas is installed locally without https it may has to be
set to **False** in instance/production.py

**Case study** is now a system type. For existing instances the database
upgrade script will add one, if not already present. In case it was used with a
different name, it should be renamed to Case study before running the upgrade
script.

### 9.1.x to 9.2.0
9.2.0.sql is needed but will be taken care of by the database upgrade script.

An additional Python package is needed:

    sudo apt install python3-fiona

Changed default `CORS_ALLOWANCE = '\*'` to
`CORS_ALLOWANCE = ''`. So if e.g. presentation sites have problems,
please add `CORS_ALLOWANCE = '\*'` or a specific IP to
the `production.py`.

### 9.0.0 to 9.1.0
9.1.0.sql is needed but will be taken care of by the database upgrade script.

Node packages are updated. Please run following command in
**openatlas/static/**

    cd openatlas/static
    npm install

### 8.15.x to 9.0.0
WARNING - this is a major release and requires software upgrades. If you are
using a Debian system upgrade it to 13 (Trixie).

Use packages from install.md after the upgrade to be sure to have the relevant
packages, for more information and instructions see
https://redmine.openatlas.eu/issues/2343.

If you upgrade a Debian system be sure to have the new postgis
packages installed (see install.md) before you upgrade database clusters.

9.0.0.sql is needed but will be taken care of by the database upgrade script.
