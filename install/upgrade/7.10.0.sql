-- Upgrade 7.9.x to 7.10.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.10.0' WHERE name = 'database_version';

-- Add check to prevent empty entity names
ALTER TABLE model.entity ADD CONSTRAINT no_empty_name CHECK (name <> '');

-- #1090 Radiocarbon Dating
UPDATE model.openatlas_class SET name = 'type_tools' WHERE name = 'type_anthropology';
UPDATE web.hierarchy SET category = 'tools' WHERE category = 'anthropology';

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
  ('E55', 'type_tools', 'Radiocarbon', 'Used for radiocarbon dating');

INSERT INTO web.hierarchy (id, name, category, multiple, directional) VALUES
  ((SELECT id FROM model.entity WHERE name='Radiocarbon'), 'Radiocarbon', 'tools', False, False);

END;
