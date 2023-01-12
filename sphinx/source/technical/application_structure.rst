Application Structure
=====================

.. toctree::

The website's software is written in `Python <https://www.python.org/>`_ and
uses the `Flask <https://palletsprojects.com/p/flask/>`_ framework.
Below you find an overview of the file structure:

* **config** - default configuration
* **files**:

    * **export** - files generated from SQL
    * **processed images** - smaller generated files which are more suitable
      for web browsers
    * **uploads** - files uploaded by users

* **install** - contains e.g. SQL files for installation:

    * **crm** - used to import the CIDOC CRM, not needed for application to run
    * **upgrade** - SQL upgrade files and information how to upgrade

* **instance** - configuration files
* **openatlas**:

    * **api**
    * **database** - the SQL code lives here
    * **display** - display manager and utility functions
    * **forms** - form manager and other forms related files
    * **models** - classes used in the application
    * **static** - the web root containing CSS, JavaScript, layout images,
      etc.
    * **templates** - HTML template files
    * **translations** - source and compiled files for translations
    * **views** - files concerning routing, redirects, etc.

* **sphinx** - source files for the user manual, used with
  `Sphinx <https://www.sphinx-doc.org/en/master/>`_
* **test**

To retrace for example a call that was made from a web browser such as
/entity/15883

* **openatlas/init.py** is processed and **before_request()** is executed
* The URL is resolved and a function in **views** is called, in this case
  **view()** from **openatlas/views/entity.py**
* Most often some model information is needed, in this case **get_by_id()**
  in **openatlas/models/entity.py**
* All SQL is located in database, so in this case **get_by_id()** in
  **openatlas/database/entity.py** is called
* A template is called from the view, in this case
  **openatlas/templates/entity/view.html**
* The template may use filters defined in **openatlas/display/util.py**
  like: some_data|some_filter


