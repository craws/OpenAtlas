-- Upgrade 7.11.0 to 7.13.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.13.0' WHERE name = 'database_version';

-- (#2007) Fix direction of preceding events (#2007)
UPDATE model.link SET domain_id = range_id, range_id = domain_id WHERE property_code = 'P134';

-- (#2009) Fix spelling errors in model
UPDATE model.property SET name = 'begins in' WHERE code = 'OA8';
UPDATE model.property SET name = 'ends in' WHERE code = 'OA9';

-- (#1952) E11 Modification
INSERT INTO model.openatlas_class (name, cidoc_class_code, alias_allowed, reference_system_allowed, new_types_allowed, write_access_group_name, layout_color, layout_icon, standard_type_id) VALUES
  ('modification', 'E11',  false, true,  true,  'contributor', '#0000FF', 'mdi-calendar', (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1));

INSERT INTO web.hierarchy_openatlas_class (hierarchy_id, openatlas_class_name) VALUES
  ((SELECT id FROM web.hierarchy WHERE name='Event'), 'modification');

END;
