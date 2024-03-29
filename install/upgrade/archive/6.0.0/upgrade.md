## INFO
Before executing SQL statements, backup the database. Replace database role
"openatlas" if needed. Older upgrade scripts and information can be found in
the archive directory.

If you are using git and want to update to the latest stable release you can
fetch the main branch e.g.

    git pull origin main

After following the instructions restart Apache and test if the application
is working.

    service apache2 restart

## New automatic upgrades

Beginning from 6.6.0 you can also use the database update script. It is still
experimental but there are no know issues and a backup is made before changes
happen. You still should read the upgrade notes about important information.

**Limitations**

* You should only do this with the official main branch of OpenAtlas.
* If the database owner is not called "openatlas" (default) you will have to
  update the SQL files accordingly before.

**Usage**

    $: git pull origin main
    #: python3 install/upgrade/database_upgrade.py
    #: service apache2 restart

### 6.5.x to 6.6.0

There were some changes in database and model (#1563). In case you depend on
direct database access for other application be sure to test these first.

Execute **install/upgrade/6.6.0.sql** after making backups.

#### Api changes

##### System Class *find*

System class ***find*** was merged with ***artifact***. Please be aware, that
this can have an impact on some API operations (e.g. **/classes**,
**/system_class/find**, etc.)

##### Versioning

A new path, which always points to the newest stable version (currently 0.2),
was added:

    /api/<endpoint>

Version 0.3 was added. It is still in development and prone to changes but can
be accessed via:

    /api/0.3/<endpoint>

### 6.4.x to 6.5.0
Install python3-rdflib and python3-rdflib-jsonld for the RDF feature (#1184):

    # apt install python3-rdflib python3-rdflib-jsonld

### 6.3.0 to 6.4.0
Execute **install/upgrade/6.4.0.sql** after making backups. This will activate
image processing to e.g. generate thumbnails.

Install python3-wand e.g. on Debian:

    # apt install python3-wand

Make the following folder writeable for the Apache user:

    openatlas/processed_images/resized

e.g:

    # chown www-data openatlas/processed_images/resized

For the new image rotate function an additional JavaScript package has to be
installed with npm. Otherwise, maps with overlays will break. Execute e.g.

    $ cd openatlas/static
    $ pip3 install -e ./
    $ ~/.local/bin/calmjs npm --install openatlas

If you get the error "not overwriting existing 'static/package.json'",
delete this file and try again.

### 6.2.x to 6.3.0
A code base update (e.g. with git pull) and an Apache restart is sufficient.

### 6.1.0 to 6.2.0
Execute **install/upgrade/6.2.0.sql** after making backups.

### 6.0.x to 6.1.0
Execute **install/upgrade/6.1.0.sql** after making backups.

### 5.7.x to 6.0.0
Execute **install/upgrade/6.0.0.sql** after making backups.

Install package needed for backup compression:

    #  apt install p7zip-full
