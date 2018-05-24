-- Upgrade to 3.6.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Add value types

ALTER TABLE web.hierarchy ADD COLUMN value_type boolean;
COMMENT ON COLUMN web.hierarchy.value_type IS 'True if links to this type can have numeric values';
ALTER TABLE web.hierarchy ALTER column value_type SET DEFAULT false;
UPDATE web.hierarchy SET value_type = false;
ALTER TABLE web.hierarchy ALTER column value_type SET NOT NULL;

INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Dimensions', 'Physical dimensions like weight and height.');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'Height', 'In centimeters'), ('E55', 'Weight', 'In gram');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Height')),
('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Weight'));
INSERT INTO web.hierarchy (id, name, value_type) VALUES ((SELECT id FROM model.entity WHERE name='Dimensions'), 'Dimensions', True);
INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES ((SELECT id FROM web.hierarchy WHERE name LIKE 'Dimensions'),(SELECT id FROM web.form WHERE name LIKE 'Find'));

-- Fix possible wrong type for "Source translation"

UPDATE model.entity SET class_code = 'E55' WHERE class_code = 'E53' and name = 'Source translation';

COMMIT;
