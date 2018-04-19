## INFO

Before executing SQL statements backup the database. Replace database role "openatlas" if needed.

### 3.3.0 to 3.4.0

Execute install/upgrade/3.4.0.sql after making backups

### 3.2.x to 3.3.0

Execute install/upgrade/3.3.0.sql after making backups

Make the openatlas/uploads directory writeable for apache e.g.

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
