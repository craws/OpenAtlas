User
====

.. toctree::

In the overview users and information on their group, email, created/last
login date, and newsletter subscription are displayed. When viewing a user
you can click on *Activity* to browse entity inserts, updates, and deletes of
this user.

Users can be added by admins or manager and a registration mail with account
details can be sent by the system if **Send account information** is checked.

Form fields
-----------
* **Active** - if not checked the user cannot log in anymore. Keeping
  inactive users saved in the system can be useful to keep associated
  information e.g. about created and modified entities
* **Group** - defines the access level of a user, see table below
* **Username** - required to login and displayed in advanced view of
  created/modified entries
* **Email** - required for e.g. resetting the password
* **Full name** - optional but makes it easier for other to be identified.
  Can be edited in :doc:`/tools/profile`.
* **Info** - a free text field for additional information

Groups
------

Guest is the default for users who aren't logged in.

+---------------------+-----+-------+------+-----------+--------+-----+
|                     |Admin|Manager|Editor|Contributor|Readonly|Guest|
+=====================+=====+=======+======+===========+========+=====+
|Browse data          |yes  |yes    |yes   |yes        |yes     |     |
+---------------------+-----+-------+------+-----------+--------+-----+
|Edit data            |yes  |yes    |yes   |yes*       |        |     |
+---------------------+-----+-------+------+-----------+--------+-----+
|Edit types           |yes  |yes    |yes   |           |        |     |
+---------------------+-----+-------+------+-----------+--------+-----+
|Add custom types     |yes  |yes    |      |           |        |     |
+---------------------+-----+-------+------+-----------+--------+-----+
|Add reference systems|yes  |yes    |      |           |        |     |
+---------------------+-----+-------+------+-----------+--------+-----+
|Import/Export        |yes  |yes    |      |           |        |     |
+---------------------+-----+-------+------+-----------+--------+-----+
|User management      |yes  |yes    |      |           |        |     |
+---------------------+-----+-------+------+-----------+--------+-----+
|System settings      |yes  |       |      |           |        |     |
+---------------------+-----+-------+------+-----------+--------+-----+

\* Contributors can edit all entries but can only delete their own.
