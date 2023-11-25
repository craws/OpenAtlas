## INFO
You can use the database update script which takes care of database changes even
over multiple versions. A backup is made before changes happen.
You still should read the upgrade notes about important information.

**Database update script limitations**
* You should only do this within the official **main** branch of OpenAtlas
* If the database owner is not called "openatlas" (default) you will have to
  update the SQL files accordingly before

**How to upgrade**
This upgrade example is written for a Linux system
* Update the code base
* Run the database upgrade script
* Restart Apache

    git pull origin main
    sudo python3 install/upgrade/database_upgrade.py
    sudo service apache2 restart

### 7.17.x to 8.0.0

This is a major upgrade which utilizes newer versions of almost every underlying
software used. Please consult the install.md about package installation.
