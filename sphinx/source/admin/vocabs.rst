Vocabs
======

.. toctree::

Available for admins and managers only.

A Vocabs import allows for an import of a controlled vocabularies as
OpenAtlas custom types from a `Skosmos <https://skosmos.org/>`_ service.

As default the `ACDH-CH Skosmos <https://vocabs.acdh.oeaw.ac.at/>`_  service
is selected.

Edit
____

* **Base URL** - Enter a valid `Skosmos <https://skosmos.org/>`_ service URL.
  Please provide the trailing slash
* **Endpoint** - Enter a valid REST API endpoint
* **User** - Enter a username, if the service needs an authentication

If an authentication is needed the password has to be provided within the
instance/production.py

``VOCABS_PW = ''``

Show vocabularies
_________________

All available vocabularies of the given service URL are displayed as table.
Each name is linked to the vocabulary at the provided service.
You can choose to import the *hierarchy* or the *collection* of a vocabulary.
For the difference please confer https://www.w3.org/TR/skos-primer/.

To import a vocabulary, click either on **hierarchy** or **groups**.

Import
______

* **Top concepts** - Select top concepts to import as custom hierarchy.
  Each child concept will be imported as type in the conceptual order.
* **Classes** - Choose to which classes the new types will be added to, e.g.
  Artifact or Place.
* **Multiple** - Decide if the type is single or multiple choice
* **Language** - Decide what language is used. If a concept name is not
  available in the choosen language, the preferred language of the vocabulary
  will be used



