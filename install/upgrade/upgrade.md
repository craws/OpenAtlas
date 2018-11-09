## INFO

Before executing SQL statements backup the database. Replace database role "openatlas" if needed.

After following the instructions restart Apache and test if the application is working.

    service apache2 restart

### 3.9.0 to 3.10.0

Install pandas libraries (needed for export and import)

    # apt-get install python3-pandas python3-geopandas python3-xlrd

Add this line to your apache config right after the WSGIScriptAlias line

    WSGIApplicationGroup %{GLOBAL}

Execute install/upgrade/3.10.0.sql after making backups

### 3.8.0 to 3.9.0

Execute install/upgrade/3.9.0.sql after making backups

### 3.7.0 to 3.8.0

For the export functions you need to make these directories writeable for the Apache user:

openatlas/export/csv

openatlas/export/sql

e.g.

    # chown www-data openatlas/uploads

You can check at /admin if there are warnings about non-writeable directories.

### 3.6.x to 3.7.0

One major change is that it isn't needed anymore to have different branches for different projects.
The master branch should be sufficient for all projects.

Execute install/upgrade/3.7.0.sql after making backups

Changes to look out for:

- Change logo function to customize the logo if you like to replace the default OpenAtlas logo
- The site header text is now a setting on its own and can be configured at admin/settings/general
- Configuration should be done in instance/production.py (not in config/default.py)

### 3.5.0 to 3.6.0

Due to a bug it was possible to link information carriers to event, actor and place. These links are
invalid and will be removed with the 3.6.0.sql update. You should check the information carriers for
those invalid links which will be deleted before executing the SQL.

Execute install/upgrade/3.6.0.sql after making backups

### 3.4.x to 3.5.0

Execute install/upgrade/3.5.0.sql after making backups

After the upgrade you can add a legal notice text if you like at admin > content > legal notice

### 3.3.x to 3.4.0

Execute install/upgrade/3.4.0.sql after making backups

### 3.2.x to 3.3.0

Execute install/upgrade/3.3.0.sql after making backups

Make the openatlas/uploads directory writable for apache e.g.

    chown www-data /var/www/net/openatlas/openatlas/uploads/

### 3.1.0 to 3.2.0

#### Database

Execute install/upgrade/3.2.0.sql after making backups

#### Apache

Update Apache config for serving static files - see install/example_apache.conf

### 3.0.0 to 3.1.0

apt-get install python3-numpy

### 2.4.1 to 3.0.0 Upgrade (PHP to Python upgrade)

Be sure to have upgraded the database to the PHP Version 2.3.2 and have read the information below.

#### Passwords

The password hash function changed to Bcrypt so all user passwords from the PHP version will be
invalid.

The mail password is not being stored in the database anymore and has to be set in
/instance/config.py (MAIL_TRANSPORT_PASSWORD). See /install/example_config.py

#### Content

Website text translations where completely rewritten.

Please backup your text translations at "Content" in the web interface and
enter them in "Settings" (intro and contact; faq was removed) again after upgrading.

#### Edition and Bibliography

Edition and bibliography types are only checked one level deep. Meaning if your
edition/bibliography subtypes have also subtypes you have to remove them or adapt the SQL.

#### Database update

Execute install/upgrade/3.0.0.sql after making backups.
