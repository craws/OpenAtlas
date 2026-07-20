BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.4.0' WHERE name = 'database_version';

-- Standard API field for DOI with Crossref (#2601, #2617)
INSERT INTO model.entity (name, cidoc_class_code, description, openatlas_class_name)
SELECT
    'DOI',
    'E32',
    'A DOI (Digital Object Identifier) is a persistent identifier for digital resources. OpenAtlas uses Crossref for autocomplete, but any DOI can be stored and resolved, even if it is not found there. Please enter only the DOI identifier itself, not the full URL or domain.',
    'reference_system'
WHERE NOT EXISTS (
    SELECT 1 FROM model.entity WHERE name='DOI' AND openatlas_class_name = 'reference_system'
);

INSERT INTO web.reference_system (system, name, api, entity_id, resolver_url, website_url, identifier_example)
VALUES (
    true,
    'DOI',
    'DOI',
    (SELECT id FROM model.entity WHERE name = 'DOI' AND openatlas_class_name = 'reference_system'),
    'https://doi.org/',
    'https://www.crossref.org/',
    '10.5281/zenodo.20451000')
ON CONFLICT (name) DO UPDATE SET resolver_url = 'https://doi.org/', system=true, api='DOI';

INSERT INTO web.reference_system_openatlas_class (reference_system_id, openatlas_class_name)
SELECT (SELECT entity_id FROM web.reference_system WHERE name='DOI'), 'edition'
WHERE NOT EXISTS (
    SELECT 1 FROM web.reference_system_openatlas_class
    WHERE
        reference_system_id=(SELECT entity_id FROM web.reference_system WHERE name='DOI')
        AND openatlas_class_name = 'edition'
);

INSERT INTO web.reference_system_openatlas_class (reference_system_id, openatlas_class_name)
SELECT (SELECT entity_id FROM web.reference_system WHERE name='DOI'), 'bibliography'
WHERE NOT EXISTS (
    SELECT 1 FROM web.reference_system_openatlas_class
    WHERE
        reference_system_id=(SELECT entity_id FROM web.reference_system WHERE name='DOI')
        AND openatlas_class_name = 'bibliography'
);

INSERT INTO web.reference_system_openatlas_class (reference_system_id, openatlas_class_name)
SELECT (SELECT entity_id FROM web.reference_system WHERE name='DOI'), 'external_reference'
WHERE NOT EXISTS (
    SELECT 1 FROM web.reference_system_openatlas_class
    WHERE
        reference_system_id=(SELECT entity_id FROM web.reference_system WHERE name='DOI')
        AND openatlas_class_name = 'external_reference'
);

INSERT INTO model.link (property_code, range_id, domain_id) VALUES (
    'P2',
    (SELECT id FROM model.entity WHERE name='exact match'),
    (SELECT id FROM model.entity WHERE name='DOI' AND openatlas_class_name = 'reference_system')
);

-- Public flag for files as type (#2780)
-- add new type
INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Public sharing allowed', 'Mark files for public sharing, e.g. on presentation sites'),
    ('E55', 'type', 'yes_temp', ''),
    ('E55', 'type', 'no_temp', '');

INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Public sharing allowed'), (SELECT id FROM model.entity WHERE name='yes_temp')),
  ('P127', (SELECT id FROM model.entity WHERE name='Public sharing allowed'), (SELECT id FROM model.entity WHERE name='no_temp'));

INSERT INTO web.hierarchy (id, name, category, multiple, directional, required) VALUES
  ((SELECT id FROM model.entity WHERE name='Public sharing allowed'), 'Public sharing allowed', 'system', False, False, True);

INSERT INTO web.hierarchy_openatlas_class (hierarchy_id, openatlas_class_name) VALUES
  ((SELECT id FROM web.hierarchy WHERE name='Public sharing allowed'), 'file');

-- map former data
INSERT INTO model.link (property_code, domain_id, range_id)
SELECT 'P2', entity_id, (SELECT id FROM model.entity WHERE name = 'yes_temp')
FROM model.file_info WHERE public = true;

INSERT INTO model.link (property_code, domain_id, range_id)
SELECT 'P2', entity_id, (SELECT id FROM model.entity WHERE name = 'no_temp')
FROM model.file_info WHERE public = false;

DROP TABLE model.file_info;

-- rename temp names
UPDATE model.entity SET name = 'Yes' WHERE name = 'yes_temp';
UPDATE model.entity SET name = 'No' WHERE name = 'no_temp';

-- Created additional indexes (#2704)
CREATE INDEX IF NOT EXISTS cidoc_class_code_idx ON model.cidoc_class (code);
CREATE INDEX IF NOT EXISTS entity_openatlas_class_name_idx ON model.entity (openatlas_class_name);
CREATE INDEX IF NOT EXISTS entity_cidoc_class_code_idx ON model.entity (cidoc_class_code);
CREATE INDEX IF NOT EXISTS gis_entity_id_idx ON model.gis (entity_id);
CREATE INDEX IF NOT EXISTS link_property_code_idx ON model.link (property_code);
CREATE INDEX IF NOT EXISTS link_domain_id_idx ON model.link (domain_id);
CREATE INDEX IF NOT EXISTS link_range_id_idx ON model.link (range_id);
CREATE INDEX IF NOT EXISTS link_type_id_idx ON model.link (type_id);
CREATE INDEX IF NOT EXISTS property_code_idx ON model.property (code);
CREATE INDEX IF NOT EXISTS property_range_class_code_idx ON model.property (range_class_code);
CREATE INDEX IF NOT EXISTS property_domain_class_code_idx ON model.property (domain_class_code);
CREATE INDEX IF NOT EXISTS user_log_user_idx ON web.user_log (user_id);
CREATE INDEX IF NOT EXISTS user_log_entity_idx ON web.user_log (entity_id);

-- Standard API field for GettyAAT (#2810)
INSERT INTO model.entity (name, cidoc_class_code, description, openatlas_class_name)
SELECT
    'Getty AAT',
    'E32',
    'Getty AAT (Art and Architecture Thesaurus) is a controlled vocabulary for art and architecture terms. AAT is a thesaurus containing generic terms, dates, relationships, sources, and notes for work types, roles, materials, styles, cultures, techniques, and other concepts related to art, architecture, and other cultural heritage (e.g., amphora, oil paint, olieverf, acetolysis, sintering, orthographic drawings, Olmeca, Rinascimento, Buddhism, watercolors, asa-no-ha-toji, sralais). Please enter only the Getty AAT identifier itself, not the full URL or domain.',
    'reference_system'
WHERE NOT EXISTS (
    SELECT 1 FROM model.entity WHERE name='Getty AAT' AND openatlas_class_name = 'reference_system'
);

INSERT INTO web.reference_system (system, name, api, entity_id, resolver_url, website_url, identifier_example)
VALUES (
    true,
    'Getty AAT',
    'GettyAAT',
    (SELECT id FROM model.entity WHERE name = 'Getty AAT' AND openatlas_class_name = 'reference_system'),
    'https://vocab.getty.edu/page/aat/',
    'https://www.getty.edu/research/tools/vocabularies/aat/',
    '300387513')
ON CONFLICT (name) DO UPDATE SET resolver_url = 'https://vocab.getty.edu/aat/', system=true, api='GettyAAT';

INSERT INTO web.reference_system_openatlas_class (reference_system_id, openatlas_class_name)
SELECT (SELECT entity_id FROM web.reference_system WHERE name='Getty AAT'), 'type'
WHERE NOT EXISTS (
    SELECT 1 FROM web.reference_system_openatlas_class
    WHERE
        reference_system_id=(SELECT entity_id FROM web.reference_system WHERE name='Getty AAT')
        AND openatlas_class_name = 'type'
);

INSERT INTO model.link (property_code, range_id, domain_id) VALUES (
    'P2',
    (SELECT id FROM model.entity WHERE name='exact match'),
    (SELECT id FROM model.entity WHERE name='Getty AAT' AND openatlas_class_name = 'reference_system')
);


-- Standard API field for Kulturpool (#2627)
INSERT INTO model.entity (name, cidoc_class_code, description, openatlas_class_name)
SELECT
    'Kulturpool',
    'E32',
    'Kulturpool is Austria''s central digital portal for art, culture, and science, aggregating millions of digital objects and metadata from nationwide museums, libraries, and archives. Administered by the Natural History Museum Vienna (NHM), it serves as the official national aggregator for the European digital platform Europeana.',
    'reference_system'
WHERE NOT EXISTS (
    SELECT 1 FROM model.entity WHERE name='Kulturpool' AND openatlas_class_name = 'reference_system'
);

INSERT INTO web.reference_system (system, name, api, entity_id, resolver_url, website_url, identifier_example)
VALUES (
    true,
    'Kulturpool',
    'Kulturpool',
    (SELECT id FROM model.entity WHERE name = 'Kulturpool' AND openatlas_class_name = 'reference_system'),
    'https://kulturpool.at/objekte/',
    'https://kulturpool.at/',
    'dfc50104-275f-44b7-aa9f-00975528a671')
ON CONFLICT (name) DO UPDATE SET resolver_url = 'https://kulturpool.at/objekte/', system=true, api='Kulturpool';

END;
