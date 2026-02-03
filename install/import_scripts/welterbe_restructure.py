"""
This script is for restructuring place hierarchies from the Welterbe project.
Basically:
* Places -> Custom hierarchy kataster
* Feature and artifacts -> Places

Steps:
* Add custom place hierarchy "Kataster"
* Link system cadaster ext ref system to admininstrative units
* Make non selectable top level Kataster entries e.g. 42005 for 42005_F407G8
* Change existing places to hierarchically place hierarchy entities
** Take care of different spellings, e.g. spaces, F and N characters, ...
** Add external reference link with correct spelling e.g. 42005/.407/8
* Change existing features and artifacts to places
* Delete place types
* Change feature and artifact types to place types
* Test everything and once looking ok upload online to be tested by others too

"""
