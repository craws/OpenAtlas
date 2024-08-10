BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.6.0' WHERE name = 'database_version';


-- #2325 Add external reference system GND (but only if it doesn't exist already)
INSERT INTO model.entity (name, cidoc_class_code, description, openatlas_class_name)
SELECT
    'GND',
    'E32',
    'GND stands for Gemeinsame Normdatei (Integrated Authority File) and offers a broad range of elements to describe authorities.',
    'reference_system'
WHERE NOT EXISTS (
    SELECT 1 FROM model.entity WHERE name='GND' AND openatlas_class_name = 'reference_system'
);

INSERT INTO web.reference_system (system, name, entity_id, resolver_url, website_url, identifier_example)
VALUES (
    true,
    'GND',
    (SELECT id FROM model.entity WHERE name = 'GND' AND openatlas_class_name = 'reference_system'),
    'https://lobid.org/gnd/',
    'https://d-nb.info/standards/elementset/gnd',
    '119338467')
ON CONFLICT (name) DO UPDATE SET resolver_url = 'https://lobid.org/gnd/', system=true;

INSERT INTO web.reference_system_openatlas_class (reference_system_id, openatlas_class_name)
SELECT (SELECT entity_id FROM web.reference_system WHERE name='GND'), 'person'
WHERE NOT EXISTS (
    SELECT 1 FROM web.reference_system_openatlas_class
    WHERE
        reference_system_id=(SELECT entity_id FROM web.reference_system WHERE name='GND'
        and openatlas_class_name = 'person')
);

END;
