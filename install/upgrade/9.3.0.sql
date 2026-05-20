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

END;
