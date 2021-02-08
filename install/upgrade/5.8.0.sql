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
((SELECT id FROM web.hierarchy WHERE name='Artificial Object'),(SELECT id FROM web.form WHERE name='Artificial Object'));

-- # Refactor modules
ALTER TABLE model.entity ADD COLUMN system_class text;
UPDATE model.entity SET system_class = 'acquisition' WHERE class_code = 'E8';
UPDATE model.entity SET system_class = 'activity' WHERE class_code ='E7';
UPDATE model.entity SET system_class = 'actor_appellation' WHERE class_code ='E82';
UPDATE model.entity SET system_class = 'appellation' WHERE class_code ='E41';
UPDATE model.entity SET system_class = 'artificial_object' WHERE class_code = 'E22' AND system_type = 'artificial object';
UPDATE model.entity SET system_class = 'bibliography' WHERE class_code ='E31' AND system_type = 'bibliography';
UPDATE model.entity SET system_class = '' WHERE class_code ='';

END;
