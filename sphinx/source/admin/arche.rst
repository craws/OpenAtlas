ARCHE
===

.. toctree::

**Be aware** this feature is experimental and only usable for a specific dataset.

`ARCHE <https://arche.acdh.oeaw.ac.at/>`_ (A Resource Centre for the HumanitiEs) is a service aimed at offering stable and persistent hosting as well as dissemination of digital research data and resources.

In order to import data from ARCHE to OpenAtlas changes to instance/production.py are needed (ask your administrator for further details):

.. code-block::
   :caption: instance/production.py

   ARCHE = {
    'id': 0,                                                  # Top collection ID (acdh:TopCollection)
    'collection_ids': [0],                                    # Sub collections ID containing metadata.json files (acdh:Collection)
    'base_url': 'https://arche-curation.acdh-dev.oeaw.ac.at/',      # Base URL to get data from
    'thumbnail_url': 'https://arche-thumbnails.acdh.oeaw.ac.at/'    # URL of ARCHE thumbnail service
    }}

The ARCHE button is displayed in the Admin/Data menu only if above data is provided.
Click on the ARCHE button to get to the overview section.

Overview
--------

Data provided in the production.py is displayed. If user belongs to the **manager** user group, a button called **Fetch** is displayed. Click **Fetch** to fetch data from ARCHE.


Fetch
-----

Data fetched from ARCHE are listed in a :doc:`/ui/table`.
Only data (based on the :doc:`/entity/artifact`), which was not imported is shown.

Click on **Import ARCHE data* to import data.
