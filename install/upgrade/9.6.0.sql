BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.6.0' WHERE name = 'database_version';

-- #2895 Add Research Organization Registry (ROR) as external reference system
INSERT INTO model.entity (name, description, openatlas_class_name)
SELECT
    'ROR',
    'The Research Organization Registry (ROR) provides open persistent identifiers for research organizations.',
    'reference_system'
WHERE NOT EXISTS (
    SELECT 1 FROM model.entity
    WHERE name = 'ROR' AND openatlas_class_name = 'reference_system');

INSERT INTO web.reference_system (
    system, name, api, entity_id, resolver_url, website_url, identifier_example)
VALUES (
    true,
    'ROR',
    'ROR',
    (SELECT id FROM model.entity
     WHERE name = 'ROR' AND openatlas_class_name = 'reference_system'),
    'https://ror.org/',
    'https://ror.org/',
    '028bsh698')
ON CONFLICT (name) DO UPDATE
SET system = true, api = 'ROR', resolver_url = 'https://ror.org/';

INSERT INTO web.reference_system_openatlas_class (
    reference_system_id, openatlas_class_name)
SELECT
    (SELECT entity_id FROM web.reference_system WHERE name = 'ROR'),
    'group'
WHERE NOT EXISTS (
    SELECT 1 FROM web.reference_system_openatlas_class
    WHERE reference_system_id =
        (SELECT entity_id FROM web.reference_system WHERE name = 'ROR')
        AND openatlas_class_name = 'group');

-- Add fuzzystrmatch extension and phonetic GIN index on model.entity.name
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;
CREATE INDEX IF NOT EXISTS entity_name_dm_idx ON model.entity USING gin (public.daitch_mokotoff(name));

END;
