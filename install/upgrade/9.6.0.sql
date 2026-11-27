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

-- #2156: Transform single _from dates (at 00:00:00) into one-day timespans
UPDATE model.entity
SET begin_to = begin_from
WHERE begin_from IS NOT NULL
  AND begin_to IS NULL
  AND begin_from::time = '00:00:00';

UPDATE model.entity
SET end_to = end_from
WHERE end_from IS NOT NULL
  AND end_to IS NULL
  AND end_from::time = '00:00:00';

UPDATE model.link
SET begin_to = begin_from
WHERE begin_from IS NOT NULL
  AND begin_to IS NULL
  AND begin_from::time = '00:00:00';

UPDATE model.link
SET end_to = end_from
WHERE end_from IS NOT NULL
  AND end_to IS NULL
  AND end_from::time = '00:00:00';

-- #2156: Set _to dates with 00:00:00 time to 23:59:59
UPDATE model.entity
SET begin_to = begin_to + INTERVAL '23 hours 59 minutes 59 seconds'
WHERE begin_to IS NOT NULL
  AND begin_to::time = '00:00:00';

UPDATE model.entity
SET end_to = end_to + INTERVAL '23 hours 59 minutes 59 seconds'
WHERE end_to IS NOT NULL
  AND end_to::time = '00:00:00';

UPDATE model.link
SET begin_to = begin_to + INTERVAL '23 hours 59 minutes 59 seconds'
WHERE begin_to IS NOT NULL
  AND begin_to::time = '00:00:00';

UPDATE model.link
SET end_to = end_to + INTERVAL '23 hours 59 minutes 59 seconds'
WHERE end_to IS NOT NULL
  AND end_to::time = '00:00:00';

-- #2885: Add fuzzystrmatch and pg_trgm extensions and search indexes on model.entity.name
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;
CREATE INDEX IF NOT EXISTS entity_name_dm_idx ON model.entity USING gin (public.daitch_mokotoff(name));
CREATE INDEX IF NOT EXISTS entity_name_trgm_idx ON model.entity USING gin (name public.gin_trgm_ops);

-- Add indexes for text annotation batch loading and filtered entity dumps
CREATE INDEX IF NOT EXISTS annotation_text_source_id_idx ON model.annotation_text USING btree (source_id, link_start);
CREATE INDEX IF NOT EXISTS entity_class_id_idx ON model.entity USING btree (openatlas_class_name, id);

END;
