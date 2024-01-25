-- Upgrade 7.16.x to 7.17.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.17.0' WHERE name = 'database_version';

-- #2094: IIIF configuration and documentation
INSERT INTO web.settings (name, value) VALUES
    ('iiif', ''),
    ('iiif_path', ''),
    ('iiif_url', ''),
    ('iiif_version', '2'),
    ('iiif_conversion', '');

END;
