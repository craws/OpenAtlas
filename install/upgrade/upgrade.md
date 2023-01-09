## INFO
Beginning from 6.6.0 you can use the database update script which takes care
of database changes even over multiple versions. A backup is made before
changes happen. You still should read the upgrade notes about important
information.

**Limitations using the database update script**

* You should only do this within the official **main** branch of OpenAtlas.
* If the database owner is not called "openatlas" (default) you will have to
  update the SQL files accordingly before.

**How to upgrade**

This upgrade example is written for a Linux system. First you update the code
base, then run the database upgrade script, then restart Apache:

    git pull origin main
    sudo python3 install/upgrade/database_upgrade.py
    sudo service apache2 restart

### 7.9.x to 7.9.2
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 7.9.0 to 7.9.1
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 7.8.x to 7.9.0
7.9.0.sql is needed but will be taken care of by the database upgrade script.

#### New file structure
In this version the following folders, including all sub folders and files,

    openatlas/uploads/
    openatlas/export/
    openatlas/processed_images/

have to be moved manually to the **files** directory, e.g. as root

    # mv openatlas/uploads/* files/uploads/
    # mv openatlas/export/sql/* files/export/
    # mv openatlas/processed_images/ files/processed_images/
    # chown -R www-data files

Clean up:

    # rm openatlas/uploads/.gitignore
    # rmdir openatlas/uploads
    # rm openatlas/export/sql/.gitignore
    # rmdir openatlas/export/sql
    # rmdir openatlas/export

Be aware, that external applications/scripts, e.g. backup scripts or
presentation sites might need adaptions too.

### 7.8.0 to 7.8.1
7.8.1.sql is needed but will be taken care of by the database upgrade script.

### 7.7.0 to 7.8.0
7.8.0.sql is needed but will be taken care of by the database upgrade script.

Like announced, the deprecated API version 0.2 was removed in this release.

### 7.6.x to 7.7.0
7.7.0.sql is needed but will be taken care of by the database upgrade script.

NPM packages need to be upgraded:

    $ cd openatlas/static
    $ rm package.json
    $ pip3 install -e ./
    $ ~/.local/bin/calmjs npm --install openatlas

The new CSV export function now provides files to download directly. So
the CSV folder isn't needed anymore and can be deleted (or moved elsewhere in
case you like to keep it). To remove it execute:

    $ rm -R openatlas/export/csv

This is the last version that will support the deprecated API version 0.2.
In case other systems are still depend on it, they should be updated to use
the 0.3 version before the next release.

### 7.5.0 to 7.6.0
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 7.4.0 to 7.5.0
7.5.0.sql is needed but will be taken care of by the database upgrade script.

### 7.3.0 to 7.4.0
7.4.0.sql is needed but will be taken care of by the database upgrade script.

The new stable API version is now 0.3 (instead 0.2). Systems using the API
(e.g. presentation sites) should be checked and adapted if needed.

NPM packages need to be upgraded for the Bootstrap upgrade:

    $ cd openatlas/static
    $ rm package.json
    $ pip3 install -e ./
    $ ~/.local/bin/calmjs npm --install openatlas

### 7.2.0 to 7.3.0
7.3.0.sql is needed but will be taken care of by the database upgrade script.

#### Database changes
The **gis** schema tables were merged into one table to the model schema
(#1631). In case external applications depend on direct database access you
should take care about that.

#### Announcement of API 0.2 deprecation
With the next release (7.4.0) the API version **0.2** will be deprecated and
version **0.3** will be the new default. Version 0.2. will still be available
(probably about 2 releases) until it will be removed.

### 7.1.x to 7.2.0
7.2.0.sql is needed but will be taken care of by the database upgrade script.

For the new map system NPM packages have to be upgraded:

    $ cd openatlas/static
    $ rm package.json
    $ pip3 install -e ./
    $ ~/.local/bin/calmjs npm --install openatlas

### 7.1.0 to 7.1.1
A code base update (e.g. with git pull) and a webserver restart is sufficient.

### 7.0.x to 7.1.0
7.1.0.sql is needed but will be taken care of by the database upgrade script.

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
