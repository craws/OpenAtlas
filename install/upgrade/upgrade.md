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

### 7.1.x to 7.2.0
Execute **install/upgrade/7.2.0.sql** after making backups

For the new map system NPM packages have to be upgraded:

    $ pip3 install calmjs
    $ cd openatlas/static
    $ pip3 install -e ./
    $ ~/.local/bin/calmjs npm --install openatlas

In case you get a warning in the last step about not overwriting existing
'../package.json', delete this file manually and try again.

### 7.1.0 to 7.1.1
A code base update (e.g. with git pull) and an Apache restart is sufficient.

### 7.0.x to 7.1.0

Execute **install/upgrade/7.1.0.sql** after making backups and reading release
notes below, there are some changes you should be aware of.

#### Update to current CIDOC CRM version 7.1.1
Because classes and properties have changed, adaptions for e.g. presentation
sites might be needed.
* Changed link for sub/super events: **P117** -> **P9**
* Merging of **actor appellation** to **appellation**
   * **P131** replaced with **P1**
   * **E82** replaced with **E41**
   * OpenAtlas class **actor appellation** removed

#### API 0.3 breaking change
* Renamed **description** to **descriptions** in LinkedPlaces Format
(standard output)

#### Mail function change
At admin/mail the port should be the default mail submission port **587**
(in most cases). If you got port **25** there, you might want to change it. You
can check the functionality with the **Send test mail** function there
afterwards.

### 6.6.x to 7.0.0
WARNING - this is a major release and requires software upgrades. If you are
using Debian upgrade it to 11 (bullseye).

Use packages from install.md after the upgrade to be sure to have the relevant
packages for the update.

If you upgrade a Debian system to bullseye be sure to have the new postgis
packages installed (see install.md) before you upgrade database clusters.

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
