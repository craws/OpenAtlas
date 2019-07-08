-- Upgrade 3.17.x to 3.18.0
-- Be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Insert additional boolean field "locked" to web.hierarchy
ALTER TABLE web.hierarchy ADD COLUMN locked boolean;
COMMENT ON COLUMN web.hierarchy.locked IS 'True if these types are not editable';
ALTER TABLE web.hierarchy ALTER column locked SET DEFAULT false;
UPDATE web.hierarchy SET locked = false;
ALTER TABLE web.hierarchy ALTER column locked SET NOT NULL;

-- Types for external references e.g. GeoNames
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'External Reference Match', 'SKOS based definition of the confidence degree that concepts can be used interchangeable.');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'exact match', 'High degree of confidence that the concepts can be used interchangeably.');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'close match', 'Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='External Reference Match'), (SELECT id FROM model.entity WHERE name='exact match')),
    ('P127', (SELECT id FROM model.entity WHERE name='External Reference Match'), (SELECT id FROM model.entity WHERE name='close match'));
INSERT INTO web.hierarchy (id, name, multiple, system, directional, value_type, locked) VALUES ((SELECT id FROM model.entity WHERE name='External Reference Match'), 'External Reference Match', False, True, False, False, True);

COMMIT;
