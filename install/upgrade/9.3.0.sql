BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.3.0' WHERE name = 'database_version';

-- Standard API field for external reference systems (#2737)
ALTER TABLE web.reference_system ADD COLUMN "api" text;
UPDATE web.reference_system SET api = 'Wikidata' WHERE name = 'Wikidata';
UPDATE web.reference_system SET api = 'GeoNames' WHERE name = 'GeoNames';
UPDATE web.reference_system SET api = 'Cadaster' WHERE name = 'Cadaster';
UPDATE web.reference_system SET api = 'GND' WHERE name = 'GND';

-- UUID (#2796)
ALTER TABLE model.entity ADD COLUMN IF NOT EXISTS uuid UUID;
UPDATE model.entity SET uuid = gen_random_uuid() WHERE uuid IS NULL;
ALTER TABLE model.entity ALTER COLUMN uuid SET NOT NULL;
ALTER TABLE model.entity ADD CONSTRAINT entity_uuid_unique UNIQUE (uuid);
ALTER TABLE model.entity ALTER COLUMN uuid SET DEFAULT gen_random_uuid();

-- Renaming OpenAtlas classes (#2718)
UPDATE model.openatlas_class SET name = 'alias' WHERE name = 'appellation';
UPDATE model.openatlas_class SET name = 'text' WHERE name = 'source_translation';
UPDATE model.entity SET name = 'Text' WHERE name = 'Source translation';
UPDATE web.hierarchy SET name = 'Text' WHERE name = 'Source translation';

-- Case study system type (#2705)
INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description)
SELECT 'E55', 'type', 'Case study', 'Mark entities for different case studies, used e.g. for presentation sites.'
WHERE NOT EXISTS (SELECT 1 FROM model.entity WHERE name='Case study' AND openatlas_class_name = 'type');

INSERT INTO web.hierarchy (id, name, category, multiple, directional)
SELECT (SELECT id FROM model.entity WHERE name='Case study'), 'Case study', 'custom', True, False
WHERE NOT EXISTS (SELECT 1 FROM web.hierarchy WHERE name='Case study');

END;
