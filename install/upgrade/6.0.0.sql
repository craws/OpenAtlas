-- Upgrade 5.7.x to 5.8.0
-- Be sure to backup the database and read the upgrade notes before executing this!

BEGIN;

-- #1456 Artificial objects
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Artificial Object', '');
INSERT INTO model.entity (class_code, name) VALUES ('E55', 'Coin'), ('E55', 'Statue');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM model.entity WHERE name='Artificial Object'), (SELECT id FROM model.entity WHERE name='Coin')),
('P127', (SELECT id FROM model.entity WHERE name='Artificial Object'), (SELECT id FROM model.entity WHERE name='Statue'));

INSERT INTO web.form (name, extendable) VALUES ('Artificial Object', True);
INSERT INTO web.hierarchy (id, name, multiple, standard, directional, value_type, locked) VALUES
((SELECT id FROM model.entity WHERE name='Artificial Object'), 'Artificial Object', False, True, False, False, False);
INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES
((SELECT id FROM web.hierarchy WHERE name='Artificial Object'), (SELECT id FROM web.form WHERE name='Artificial Object'));

-- If you executed above at an upgrade of a development version before use this instead
-- UPDATE model.entity SET name = 'Artifact' WHERE name = 'Artificial Object';
-- UPDATE model.entity SET system_type = 'artifact' WHERE system_type = 'artificial object';
-- UPDATE web.form SET name = 'Artifact' WHERE name = 'Artificial Object';

-- #1091 Reference systems for types
INSERT INTO web.form (name, extendable) VALUES ('Type', True);

-- # Refactor modules
ALTER TABLE model.entity ADD COLUMN system_class text;
UPDATE model.entity SET system_class = 'acquisition' WHERE class_code = 'E8';
UPDATE model.entity SET system_class = 'activity' WHERE class_code ='E7';
UPDATE model.entity SET system_class = 'actor_appellation' WHERE class_code = 'E82';
UPDATE model.entity SET system_class = 'appellation' WHERE class_code = 'E41';
UPDATE model.entity SET system_class = 'artifact' WHERE class_code = 'E22' AND system_type IN ('artificial object', 'artifact');
UPDATE model.entity SET system_class = 'bibliography' WHERE class_code = 'E31' AND system_type = 'bibliography';
UPDATE model.entity SET system_class = 'edition' WHERE class_code = 'E31' AND system_type = 'edition';
UPDATE model.entity SET system_class = 'external_reference' WHERE class_code = 'E31' AND system_type = 'external reference';
UPDATE model.entity SET system_class = 'feature' WHERE class_code = 'E18' AND system_type = 'feature';
UPDATE model.entity SET system_class = 'file' WHERE class_code = 'E31' AND system_type = 'file';
UPDATE model.entity SET system_class = 'find' WHERE class_code = 'E22' AND system_type = 'find';
UPDATE model.entity SET system_class = 'group' WHERE class_code = 'E74';
UPDATE model.entity SET system_class = 'human_remains' WHERE class_code = 'E20' AND system_type = 'human remains';
UPDATE model.entity SET class_code = 'E22', system_class = 'artifact' WHERE class_code = 'E84';
UPDATE model.entity SET system_class = 'legal_body' WHERE class_code = 'E40';
UPDATE model.entity SET system_class = 'location' WHERE class_code = 'E53' AND system_type IS NULL;
UPDATE model.entity SET system_class = 'move' WHERE class_code = 'E9';
UPDATE model.entity SET system_class = 'object_location' WHERE class_code = 'E53' AND system_type = 'place location';
UPDATE model.entity SET system_class = 'person' WHERE class_code = 'E21';
UPDATE model.entity SET system_class = 'place' WHERE class_code = 'E18' AND system_type = 'place';
UPDATE model.entity SET system_class = 'reference_system' WHERE class_code = 'E32';
UPDATE model.entity SET system_class = 'source' WHERE class_code = 'E33' AND system_type = 'source content';
UPDATE model.entity SET system_class = 'stratigraphic_unit' WHERE class_code = 'E18' AND system_type = 'stratigraphic unit';
UPDATE model.entity SET system_class = 'translation' WHERE class_code = 'E33' AND system_type = 'source translation';
UPDATE model.entity SET system_class = 'type' WHERE class_code = 'E55';

ALTER TABLE model.entity ALTER COLUMN system_class SET NOT NULL;
-- ALTER TABLE model.entity DROP COLUMN system_type;

END;
