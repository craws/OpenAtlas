Features
========

OpenAtlas is developed for easy acquisition, editing, and management of
research data from the humanities as well as related research fields. Special
emphasis is placed on making data entry as easy and convenient as possible for
researchers while maintaining high standards in the development of the
software. The features listed below contribute significantly to this effort.

Model
-----

The data model specifies the structure in which the information is stored
within the database. The use of an ontology, for example, allows the data to be
combined more easily with information from other projects and is consistent
with the `FAIR principles <https://www.go-fair.org/fair-principles/>`_.

The OpenAtlas :doc:`/model/index` is based on the international standard of
`CIDOC CRM <https://www.cidoc-crm.org/>`_, an ontology widely used within the
field of humanities.

* :doc:`Types </entity/type>` can be used to adapt for specific research topics
* :doc:`Reference Systems </entity/reference_system>` for
  Linked Open Data (LOD)
* Mapping :doc:`spatial </tools/map>` and
  :doc:`temporal </ui/date>` uncertainty
* :doc:`Archaeological finds </examples/archaeological_data>`
  with detailed mapping
* :doc:`Data integrity check</admin/data_integrity_checks>` functions
* :doc:`Model link checker<model/link_checker>` to confirm CIDOC CRM validity

User interface
--------------

The user interface allows for easy and quick entry of information into the
database, while the data is mapped in the background according to the
specifications of the data model (see above).
Due to the use of :doc:`types </entity/type>`, this can be designed
particularly flexibly and can thus be adapted to the requirements of each
project.

* :doc:`Interactive map </tools/map>` to enter places with a known location
* :doc:`File upload </entity/file>`
* :doc:`/tools/search` and :doc:`table </ui/table>` filter functions for quick
  navigation
* :doc:`/tools/network`
* :doc:`/tools/notes` and bookmarks
* :doc:`User manual </index>` (English) with :doc:`examples </examples/index>`
  and context specific links in the application
* User interface internationalization using
  `gettext <https://www.gnu.org/software/gettext/>`_, currently implemented:

   * Catalan
   * English
   * German
   * Spanish

.. image:: /ui.png

Data exchange
-------------

OpenAtlas offers various possibilities to exchange data with other systems or
to import data into the database system.

* :doc:`/technical/api` for easier exchange with other information system
* :doc:`/admin/export` functions for multiple formats
* :doc:`/admin/import` of CSV files

User management
---------------

The User Management Features allows the activation of users for the own
OpenAtlas instance. These can also be divided into different user groups with
different permissions. In addition, the user interface can be adapted to the
user's own preferences via settings.

* :doc:`/admin/user` and groups can be used to grant different access levels
* :doc:`/tools/profile` settings to adapt for personal workflows
* Newsletter function with automated unsubscribe links
* Password reset

Anthropological Analyses
------------------------

In order to also allow interdisciplinary work with anthropological data,
anthropological methods, such as age and sex determination, will be available
in OpenAtlas in the future. The implementation of the age determination
according to Ferembach et al. is the first step in this direction.

* :doc:`Sex estimation </tools/anthropological_analyses>` based on the method
  given by Ferembach et al. 1979
