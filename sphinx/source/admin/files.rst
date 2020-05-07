Files
=====

.. toctree::

Settings

* **Maximum file size in MB**
* **Profile image width in pixel** - this only influences the layout of info tabs
* **Allowed file extensions** - enter file extensions witout a dot and separated with a space e.g.

.. code-block:: python

  gif jpg jpeg

Images that can be displayed in the browser are defined through their extensions and can be changed
in the configuration file (e.g. instance/production.py) default is:

.. code-block:: python

   DISPLAY_FILE_EXTENSIONS = ['bmp', 'gif', 'ico', 'jpeg', 'jpg', 'png', 'svg']
