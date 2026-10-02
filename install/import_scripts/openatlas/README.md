# About
This script can be used to merge an OpenAtlas instance into an existing one.

The script is still very basic but will be expanded on a need to basis, feel
free to add feature request at our
[Redmine](https://redmine.openatlas.eu/projects/uni/wiki)

# Preparation and usage
The database and files to be imported into are the ones configured in this
instance, so be sure to check the configuration in **instance/production.py**:

The database and files to be imported from are configured at the top of the
**merge.py** script.

As always, be sure to make backups before. The script can be run, e.g.
from the project root with:

    python3 install/import_scripts/openatlas/merge.py
   
# Clean up
At the start of the script possible entries from the last run will be
removed. This can be useful in case you have to run the script more often to
get it right. Copied files are not cleaned up will be overridden when the
script is run again.

# New case study
A new case study will be created and will be linked to entities that are
imported. The name and description of the case study can be configured in the
script.

# What is imported

## Types
The script compares the new types with existing ones. In case there are types
with the same name in the same hierarchy the existing ones will be used and
their classes extended, in case there were more configured.

So it is a good idea to compare the type hierarchies and adapt these if needed
in the database that is to be imported before.

## Reference systems
Currently new ones won't be added but existing ones with the same name will
be mapped accordingly.

## Entities
All entities (except types and reference systems) will be imported. Currently,
there is no possibility to avoid duplicates e.g. for person, places ...
although this is already planned to do.

## Links
All links will be imported and a delete link duplicates function is called
afterward to avoid them.

## Files
If a source directory
(the fiels/upload directory of the project to be imported) is configured in the
script, the script tries to copy entries according to imported file entities
and save them with their new id.

# What is not imported
* Users and their information
* Site settings, e.g. the site name and intro text
