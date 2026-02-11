BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.1.0' WHERE name = 'database_version';

-- Remove overlay option (#2703)
DELETE FROM web.settings WHERE name = 'module_map_overlay';
DELETE FROM web.user_settings WHERE name = 'module_map_overlay';

-- Add Austrian cadastre (#2290)
INSERT INTO model.entity (name, cidoc_class_code, description, openatlas_class_name) VALUES
    ('Cadaster', 'E32', 'Austrian cadastre from the Federal Office of Metrology and Surveying Austria', 'reference_system');

INSERT INTO web.reference_system (system, name, entity_id, resolver_url, website_url, identifier_example)
VALUES (
    true,
    'Cadaster',
    (SELECT id FROM model.entity WHERE name = 'Cadaster' AND cidoc_class_code = 'E32'),
    'https://kataster.bev.gv.at/api/gst/',
    'https://kataster.bev.gv.at/',
    '01004/781/1');

INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P2', (SELECT id FROM model.entity WHERE name='exact match'), (SELECT id FROM model.entity WHERE name='Cadaster'));

END;
