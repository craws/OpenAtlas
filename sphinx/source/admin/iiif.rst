IIIF
====

.. toctree::

`IIIF <https://iiif.io/>`_ is a set of open standards for delivering
high-quality, attributed digital objects online at scale. Once installed
(see installations notes) it can be configured in the admin area at the
**IIIF** tab.

**Be aware that**

* IIIF is **optional** for an OpenAtlas installation
* Although already working and in use we still consider it **experimental**
* Enabling it can **expose** used files to the public (without login)

**Configuration**

* **IIIF** - Select this checkbox to enable IIIF
* **URL** - Set the complete URL to the Image API Server, e.g.
  **https://yourserver.eu/iiif/**
* **Version** - The manifest version provided by OpenAtlas. Currently only
  version 2 is available.
* **Path** - Set the absolute path to the IIIF image drop zone which
  corresponds with the Image API Server folder, e.g. **/var/www/iipsrv/** if
  you followed the default OpenAtlas installation. Be aware that this folder
  has to be accessible (write and execute) for the webserver.
* **Conversion** - Controls if images get converted into pyramid-TIFFs

  * **none** - no conversion
  * **deflate** - lossless but files size may be large
  * **jpeg** - much smaller files size but not lossless

In case you are running multiple OpenAtlas instances you should create a sub
directory for every instance at **/var/www/iipsrv/** and also add these to
**URL** and **Path** accordingly.

These formats have been successfully tested with OpenAtlas:

* .bmp
* .gif
* .ico
* .jpeg
* .jpg
* .png
* .svg
* .tif
* .tiff
