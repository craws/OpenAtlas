## INFO

Before executing SQL statements make a backup of the database.

Replace database role "openatlas" if needed.

### 3.0.0 to 3.1.0

apt-get install python3-numpy

### 2.4.1 to 3.0.0 Upgrade (PHP to Python upgrade)

Be sure to have upgraded the database to the PHP Version 2.3.2 and have read this document before
upgrading the database.

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

Execute 3.0.0.sql after making backups.
