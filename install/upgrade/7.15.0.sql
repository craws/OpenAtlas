-- Upgrade 7.14.0 to 7.15.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.15.0' WHERE name = 'database_version';

-- (#1991) Import controlled vocabularies via API
INSERT INTO web.settings (name, value) VALUES
    ('vocabs_base_url', 'https://vocabs.acdh.oeaw.ac.at/'),
    ('vocabs_endpoint', 'rest/v1/'),
    ('vocabs_user', '');

END;
