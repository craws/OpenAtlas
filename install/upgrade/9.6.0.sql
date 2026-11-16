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

-- Add ORCID as external reference system
INSERT INTO model.entity (name, description, openatlas_class_name)
SELECT
    'ORCID',
    'ORCID (Open Researcher and Contributor ID) provides persistent digital identifiers that distinguish researchers and contributors.',
    'reference_system'
WHERE NOT EXISTS (
    SELECT 1 FROM model.entity
    WHERE name = 'ORCID' AND openatlas_class_name = 'reference_system');

INSERT INTO web.reference_system (
    system, name, api, entity_id, resolver_url, website_url, identifier_example)
VALUES (
    true,
    'ORCID',
    'ORCID',
    (SELECT id FROM model.entity
     WHERE name = 'ORCID' AND openatlas_class_name = 'reference_system'),
    'https://orcid.org/',
    'https://orcid.org/',
    '0000-0001-7608-7446')
ON CONFLICT (name) DO UPDATE
SET system = true, api = 'ORCID', resolver_url = 'https://orcid.org/';

INSERT INTO web.reference_system_openatlas_class (
    reference_system_id, openatlas_class_name)
SELECT
    (SELECT entity_id FROM web.reference_system WHERE name = 'ORCID'),
    'person'
WHERE NOT EXISTS (
    SELECT 1 FROM web.reference_system_openatlas_class
    WHERE reference_system_id =
        (SELECT entity_id FROM web.reference_system WHERE name = 'ORCID')
        AND openatlas_class_name = 'person');

END;
