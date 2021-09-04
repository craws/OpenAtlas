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

### 6.4.1 to 6.5.0
Install python3-rdflib and python3-rdflib-jsonld for the RDF feature:

    # apt install python3-rdflib python3-rdflib-jsonld

### 6.4.0 to 6.4.1
A code base update (e.g. with git pull) and an Apache restart is sufficient.

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

### 6.2.0 to 6.2.1
A code base update (e.g. with git pull) and an Apache restart is sufficient.

### 6.1.0 to 6.2.0
Execute **install/upgrade/6.2.0.sql** after making backups.

### 6.0.x to 6.1.0
Execute **install/upgrade/6.1.0.sql** after making backups.

### 5.7.x to 6.0.0
Execute **install/upgrade/6.0.0.sql** after making backups.

Install package needed for backup compression:

    #  apt install p7zip-full
