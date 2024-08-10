BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.6.0' WHERE name = 'database_version';


-- #2325 Add external reference system GND (but only if it doesn't exist already)
INSERT INTO model.entity (name, cidoc_class_code, description, openatlas_class_name)
SELECT
    'GND',
    'E32',
    'A collection of cultural and research authority data in the German-speaking countries.',
    'reference_system'
WHERE NOT EXISTS (
    SELECT 1 FROM model.entity WHERE name='GND'
);

INSERT INTO web.reference_system (system, name, entity_id, resolver_url, website_url, identifier_example)
SELECT
    true,
    'GND',
    (SELECT id FROM model.entity WHERE name = 'GND' AND cidoc_class_code = 'E32'),
    'https://lobid.org/gnd/',
    'https://d-nb.info/gnd/',
    '119338467'
WHERE NOT EXISTS (
    SELECT 1 FROM web.reference_system WHERE name='GND'
);

INSERT INTO web.reference_system_openatlas_class (reference_system_id, openatlas_class_name)
SELECT (SELECT entity_id FROM web.reference_system WHERE name='GND'), 'person'
WHERE NOT EXISTS (
    SELECT 1 FROM web.reference_system_openatlas_class
    WHERE
        reference_system_id=(SELECT entity_id FROM web.reference_system WHERE name='GND'
        and openatlas_class_name = 'person')
);

END;
