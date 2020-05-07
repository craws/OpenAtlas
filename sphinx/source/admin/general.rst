General
=======

.. toctree::

* **Site name** - the name of the site. Displayed in browser tabs and used in emails.
* **Default language** - user can change their preferred language in the :doc:`/tools/profile`.
* **Default table rows** - user can set their preferred value in the :doc:`/tools/profile`
* **Log level**  - how much should be logged. For now only info, notice and error are used
* **Debug mode** - if turned on some debug information is displayed in the top right and DataTables stateSave option is turned off

h2. Authentications

* Random password length - the length of generated passwords at password reset or user creation
* Minimum password length - the minimum length of provided passwords at password change or user creation
* Reset confirm hours - how long a requested password reset code is valid
* Failed logins - how often it could be tried to login with a specific username
* Failed login forget minutes - how many minutes to wait to be able to try again after failed logins are exceeded

h2. Search

For live search in tables or trees a minimum character threshold can be entered. The default is 1 but it can be useful to raise it when dealing with huge datasets.

* Minimum jstree search - the minimum characters that have to be entered to filter trees e.g. types
* Minimum tablesorter search - the minimum characters that have to be entered to filter tables e.g. actors
